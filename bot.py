from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.start import start_handler
from handlers.convert import convert_handler
from handlers.stats import stats_handler
from server import start_flask

# Initialize Bot
bot = Client(
    "video_converter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Add Handlers
bot.add_handler(start_handler)
bot.add_handler(convert_handler)
bot.add_handler(stats_handler)

# Run Bot
if __name__ == "__main__":
    start_flask()  # Fake HTTP Server for Koyeb Health Check
    bot.run()
