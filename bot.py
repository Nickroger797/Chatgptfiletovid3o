import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.start import register_start_handler
from handlers.convert import register_convert_handler
from handlers.stats import register_stats_handler
import database  # ✅ Database connection import

# ✅ Debugging Mode Enable (Logs देखने के लिए)
logging.basicConfig(level=logging.DEBUG)

# ✅ Check MongoDB Connection
try:
    database.client.server_info()
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Error:", e)
    exit(1)  # Bot को बंद कर दो अगर database connect नहीं हुआ

# ✅ Initialize Bot
bot = Client(
    "video_converter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Register All Handlers
def register_handlers():
    register_start_handler(bot)
    register_convert_handler(bot)
    register_stats_handler(bot)

# ✅ Run Bot
if __name__ == "__main__":
    register_handlers()
    bot.run()
  
