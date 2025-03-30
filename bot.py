import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import database  # ✅ MongoDB Connection
import command  # ✅ Import Commands (Handlers Automatically Registered)

# ✅ Debugging Mode Enable
logging.basicConfig(level=logging.DEBUG)

# ✅ Check MongoDB Connection
try:
    database.client.server_info()
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

# ✅ Run Bot
if __name__ == "__main__":
    bot.run()
