import logging
import os
import re
import ffmpeg
import uuid
import database
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URL
from pymongo import MongoClient

# ✅ Debugging Mode Enable
logging.basicConfig(level=logging.DEBUG)

# ✅ MongoDB Connection
try:
    client = MongoClient(MONGO_URL)
    db = client["video_converter"]
    users_col = db["users"]
    logs_col = db["conversion_logs"]
    client.server_info()
    print("\u2705 MongoDB Connected Successfully!")
except Exception as e:
    print("\u274c MongoDB Connection Error:", e)
    exit(1)

# ✅ Initialize Bot
bot = Client(
    "video_converter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Temporary Filename Store
file_store = {}

# ✅ Filename Cleaner
def clean_filename(filename):
    return re.sub(r'[^\w.-]', '_', filename)

# ✅ Video Conversion Function
def convert_video(input_path, output_format, resolution, audio_format):
    output_path = input_path.rsplit(".", 1)[0] + f"_converted.{output_format}"
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec="libx264",
                b=resolution,
                acodec=audio_format,
                preset="ultrafast",  # ✅ Faster Encoding
                threads=4,  # ✅ Limit CPU Usage
                crf=23,  # ✅ Optimize Quality & Speed
                movflags="+faststart"  # ✅ Enable Fast Streaming
            )
            .run(cmd="/usr/bin/ffmpeg", overwrite_output=True)
        )
        return output_path
    except Exception as e:
        logging.error(f"FFmpeg Error: {e}")
        return None

# ✅ Start Command
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    await message.reply_text("\ud83d\udc4b Welcome! Send me a video file, and I'll convert it for you.")

# ✅ Video Upload Handler
@bot.on_message(filters.video | filters.document)
async def video_handler(client, message):
    user_id = message.from_user.id
    file_path = await message.download()
    
    # ✅ फाइल को क्लीन नाम दें
    clean_path = os.path.join(os.path.dirname(file_path), clean_filename(os.path.basename(file_path)))
    os.rename(file_path, clean_path)

    # ✅ Unique ID बनाएं और फाइल स्टोर करें
    file_id = str(uuid.uuid4())[:8]  # छोटा 8-character ID
    file_store[file_id] = clean_path

    # ✅ Format Select बटन भेजें
    buttons = [
        [InlineKeyboardButton("MP4", callback_data=f"format_mp4_{file_id}"),
         InlineKeyboardButton("MKV", callback_data=f"format_mkv_{file_id}")],
        [InlineKeyboardButton("AVI", callback_data=f"format_avi_{file_id}")]
    ]
    
    await message.reply_text("Select video format:", reply_markup=InlineKeyboardMarkup(buttons))

# ✅ Format Selection Handler
@bot.on_callback_query(filters.regex("^format_"))
async def format_handler(client, callback_query):
    format_choice, file_id = callback_query.data.split("_", 2)[1:]

    # ✅ फाइल पाथ को Retrieve करें
    file_path = file_store.get(file_id)
    if not file_path:
        await callback_query.message.edit_text("⚠ File not found. Please re-upload.")
        return

    # ✅ Resolution Select बटन भेजें
    resolutions = [
        [InlineKeyboardButton("240p", callback_data=f"res_240p_{format_choice}_{file_id}"),
         InlineKeyboardButton("360p", callback_data=f"res_360p_{format_choice}_{file_id}")],
        [InlineKeyboardButton("480p", callback_data=f"res_480p_{format_choice}_{file_id}"),
         InlineKeyboardButton("720p", callback_data=f"res_720p_{format_choice}_{file_id}")]
    ]
    
    await callback_query.message.edit_text("Select video quality:", reply_markup=InlineKeyboardMarkup(resolutions))

# ✅ Resolution Selection Handler
@bot.on_callback_query(filters.regex("^res_"))
async def resolution_handler(client, callback_query):
    res_choice, format_choice, file_id = callback_query.data.split("_", 3)[1:]

    # ✅ फाइल पाथ को Retrieve करें
    file_path = file_store.get(file_id)
    if not file_path:
        await callback_query.message.edit_text("⚠ File not found. Please re-upload.")
        return

    audio_formats = [
        [InlineKeyboardButton("MP3", callback_data=f"audio_mp3_{res_choice}_{format_choice}_{file_id}"),
         InlineKeyboardButton("AAC", callback_data=f"audio_aac_{res_choice}_{format_choice}_{file_id}")],
        [InlineKeyboardButton("WAV", callback_data=f"audio_wav_{res_choice}_{format_choice}_{file_id}")]
    ]
    
    await callback_query.message.edit_text("Select audio format:", reply_markup=InlineKeyboardMarkup(audio_formats))

# ✅ Stats Command
@bot.on_message(filters.command("stats"))
async def stats_handler(client, message):
    total_users = users_col.count_documents({})
    total_conversions = logs_col.count_documents({})
    await message.reply_text(f"\ud83d\udcca **Bot Stats**:\n\ud83d\udc65 Total Users: {total_users}\n\ud83c\udfa5 Total Conversions: {total_conversions}")

# ✅ Run Bot
if __name__ == "__main__":
    bot.run()
    
