import logging
import importlib
import os
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import database

# ✅ Debugging Mode Enable (Logs देखने के लिए)
logging.basicConfig(level=logging.DEBUG)

# ✅ Initialize Bot
bot = Client(
    "video_converter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Automatically Load All Handlers from 'handlers' Folder
def register_handlers():
    handlers_folder = "handlers"
    for filename in os.listdir(handlers_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{handlers_folder}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "register"):
                    module.register(bot)  # Call register function inside each handler
                    logging.info(f"✔ Loaded: {module_name}")
            except Exception as e:
                logging.error(f"❌ Error loading {module_name}: {e}")

# ✅ Run Bot
if __name__ == "__main__":
    register_handlers()
    bot.run()
