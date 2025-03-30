from pyrogram import Client, filters
from pyrogram.types import Message
from database import users_col, logs_col

# ✅ Stats Handler
@Client.on_message(filters.command("stats"))
async def stats_handler(client: Client, message: Message):
    total_users = users_col.count_documents({})
    total_conversions = logs_col.count_documents({})
    
    await message.reply_text(
        f"📊 **Bot Stats**:\n"
        f"👥 Total Users: {total_users}\n"
        f"🎥 Total Conversions: {total_conversions}"
    )

# ✅ Handler को Register करने का सही तरीका
def register_stats_handler(bot: Client):
    bot.add_handler(stats_handler)
