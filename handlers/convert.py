from pyrogram import Client, filters
from pyrogram.types import Message
from utils.ffmpeg_util import convert_video
from database import logs_col
import os

async def convert_handler(client: Client, message: Message):
    user_id = message.from_user.id
    if not message.video and not message.document:
        await message.reply_text("⚠️ Please send a video file.")
        return
    
    file_path = await message.download()
    output_path = convert_video(file_path)
    
    await message.reply_video(video=output_path, caption="✅ Here is your converted video!", supports_streaming=True)
    os.remove(file_path)
    os.remove(output_path)
    
    logs_col.insert_one({"user_id": user_id, "file": message.document.file_name if message.document else "video", "status": "converted"})

convert_handler = (filters.video | filters.document, convert_handler)
