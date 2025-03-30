from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize Bot
bot = Client(
    "video_converter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start Command Handler
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("Hello! I am your Video Converter Bot. Send me a file to convert.")

# Convert Handler
@bot.on_message(filters.video | filters.document)
async def convert_handler(client, message):
    await message.reply_text("Processing your file...")

# Stats Command Handler
@bot.on_message(filters.command("stats"))
async def stats_handler(client, message):
    await message.reply_text("Bot Stats: \nTotal Users: 100\nTotal Conversions: 500")

# Run Bot
if __name__ == "__main__":
    bot.run()
