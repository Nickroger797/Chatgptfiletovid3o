from pyrogram import Client, filters
from pyrogram.types import Message
from database import users_col

async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    await message.reply_text("👋 Welcome! Send me a video file, and I'll convert it to Telegram's gallery mode.")

# ✅ सही तरीका: Handler को register करने का
def register_start_handler(bot: Client):
    bot.add_handler(Client.on_message(filters.command("start"))(start_handler))
