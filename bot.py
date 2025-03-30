import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.start import register_start_handler
from handlers.convert import register_convert_handler
from handlers.stats import register_stats_handler

# ✅ Debugging Mode Enable (Logs देखने के लिए)
logging.basicConfig(level=logging.DEBUG)

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
