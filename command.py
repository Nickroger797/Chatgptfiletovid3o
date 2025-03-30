from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import users_col, logs_col

@Client.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    
    await message.reply_text(
        "👋 Welcome! Send me a video file, and I'll convert it to Telegram's gallery mode.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📌 Support", url="https://t.me/support")]
        ])
    )

@Client.on_message(filters.video | filters.document)
async def convert_handler(client: Client, message: Message):
    if not message.video and not message.document:
        await message.reply_text("⚠️ Please send a video file.")
        return
    
    file_path = await message.download()
    output_path = convert_video(file_path)
    
    await message.reply_video(
        video=output_path, 
        caption="✅ Here is your converted video!", 
        supports_streaming=True
    )
    
    os.remove(file_path)
    os.remove(output_path)

    logs_col.insert_one({"user_id": message.from_user.id, "file": "video", "status": "converted"})

@Client.on_message(filters.command("stats"))
async def stats_handler(client: Client, message: Message):
    total_users = users_col.count_documents({})
    total_conversions = logs_col.count_documents({})
    
    await message.reply_text(f"📊 **Bot Stats**:\n👥 Total Users: {total_users}\n🎥 Total Conversions: {total_conversions}")
