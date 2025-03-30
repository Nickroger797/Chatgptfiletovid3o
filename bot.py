import logging
import os
import ffmpeg
import database
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from pymongo import MongoClient
from config import MONGO_URL

# ✅ Debugging Mode Enable
logging.basicConfig(level=logging.DEBUG)

# ✅ MongoDB Connection
try:
    client = MongoClient(MONGO_URL)
    db = client["video_converter"]
    users_col = db["users"]
    logs_col = db["conversion_logs"]
    client.server_info()
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Error:", e)
    exit(1)

# ✅ Initialize Bot
bot = Client(
    "video_converter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Start Command
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    await message.reply_text("👋 Welcome! Send me a video file, and I'll convert it to Telegram's gallery mode.")

# ✅ Convert Video Function
def convert_video(input_path):
    output_path = input_path.replace(".mp4", "_converted.mp4")  # नया नाम
    try:
        ffmpeg.input(input_path).output(output_path, vcodec="libx264", preset="ultrafast").run()
        return output_path
    except Exception as e:
        logging.error(f"FFmpeg Error: {e}")
        return None

# ✅ Video Convert Handler
@bot.on_message(filters.video | filters.document)
async def convert_handler(client, message):
    user_id = message.from_user.id

    if not message.video and not message.document:
        await message.reply_text("⚠️ Please send a video file.")
        return

    # ✅ सबसे पहले यूज़र को रिप्लाई करो कि वीडियो कन्वर्ट हो रही है
    processing_msg = await message.reply_text("⏳ Your file is being converted, please wait...")

    file_path = await message.download()
    output_path = convert_video(file_path)

    if output_path:
        await client.send_video(
            chat_id=message.chat.id,
            video=output_path,
            caption="✅ Here is your converted video!",
            supports_streaming=True
        )
        os.remove(file_path)
        os.remove(output_path)
        logs_col.insert_one({"user_id": user_id, "status": "converted"})
    else:
        await message.reply_text("❌ Conversion failed. Please try again.")

    # ✅ "Converting..." वाले message को हटा दो
    await processing_msg.delete()

# ✅ Stats Command
@bot.on_message(filters.command("stats"))
async def stats_handler(client, message):
    total_users = users_col.count_documents({})
    total_conversions = logs_col.count_documents({})
    await message.reply_text(f"📊 **Bot Stats**:\n👥 Total Users: {total_users}\n🎥 Total Conversions: {total_conversions}")

# ✅ Run Bot
if __name__ == "__main__":
    bot.run()
