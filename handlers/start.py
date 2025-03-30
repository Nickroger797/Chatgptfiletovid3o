from pyrogram import Client, filters
from pyrogram.types import Message
from database import users_col

# ✅ Start Command Handler
@Client.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    await message.reply_text("👋 Welcome! Send me a video file, and I'll convert it to Telegram's gallery mode.")

# ✅ Handler को Register करने का सही तरीका
def register_start_handler(bot: Client):
    bot.add_handler(start_handler)
