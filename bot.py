import logging
import os
import re
import ffmpeg
import database
from pyrogram import Client, filters
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

# ✅ फाइल का नाम क्लीन करने का फ़ंक्शन
def clean_filename(filename):
    return re.sub(r'[^\w.-]', '_', filename)  # केवल letters, numbers, underscore, dot और hyphen रहने दें

# ✅ वीडियो रीमक्स करने का फ़ंक्शन
def remux_video(input_path):
    temp_output = input_path.rsplit(".", 1)[0] + "_remuxed.mkv"
    try:
        (
            ffmpeg
            .input(input_path, err_detect="ignore_err")
            .output(temp_output, c="copy", map="0")
            .run(cmd="/usr/bin/ffmpeg", overwrite_output=True)
        )
        return temp_output
    except Exception as e:
        logging.error(f"Remux Error: {e}")
        return None

# ✅ वीडियो कन्वर्ज़न करने का फ़ंक्शन
def convert_video(input_path):
    output_path = input_path.rsplit(".", 1)[0] + "_converted.mp4"
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec="libx264",
                b="1000k",
                acodec="aac",
                audio_bitrate="128k",
                y=None
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
    await message.reply_text("\ud83d\udc4b Welcome! Send me a video file, and I'll convert it to Telegram's gallery mode.")

# ✅ Video Convert Handler
@bot.on_message(filters.video | filters.document)
async def convert_handler(client, message):
    user_id = message.from_user.id

    if not message.video and not message.document:
        await message.reply_text("\u26a0\ufe0f Please send a video file.")
        return

    processing_msg = await message.reply_text("\u23f3 Your file is being converted, please wait...")
    
    file_path = await message.download()
    clean_path = os.path.join(os.path.dirname(file_path), clean_filename(os.path.basename(file_path)))
    os.rename(file_path, clean_path)
    file_path = clean_path
    
    file_path = remux_video(file_path) or file_path  # रीमक्स करके सही करो
    output_path = convert_video(file_path)

    if output_path:
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            caption="\u2705 Here is your converted video!",
            supports_streaming=True
        )
        
        try:
            os.remove(file_path)
            os.remove(output_path)
        except Exception as e:
            logging.error(f"File Delete Error: {e}")

        logs_col.insert_one({"user_id": user_id, "status": "converted"})
    else:
        await message.reply_text("\u274c Conversion failed. Please try again.")
    
    await processing_msg.delete()

# ✅ Stats Command
@bot.on_message(filters.command("stats"))
async def stats_handler(client, message):
    total_users = users_col.count_documents({})
    total_conversions = logs_col.count_documents({})
    await message.reply_text(f"\ud83d\udcca **Bot Stats**:\n\ud83d\udc65 Total Users: {total_users}\n\ud83c\udfa5 Total Conversions: {total_conversions}")

# ✅ Run Bot
if __name__ == "__main__":
    bot.run()
