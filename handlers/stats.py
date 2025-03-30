from pyrogram import Client, filters
from pyrogram.types import Message
from database import users_col, logs_col

async def stats_handler(client: Client, message: Message):
    total_users = users_col.count_documents({})
    total_conversions = logs_col.count_documents({})
    
    await message.reply_text(f"📊 **Bot Stats**:\n👥 Total Users: {total_users}\n🎥 Total Conversions: {total_conversions}")

stats_handler = filters.command("stats")(stats_handler)
