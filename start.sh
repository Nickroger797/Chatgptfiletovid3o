#!/bin/bash

# Update and Install FFmpeg
apt update && apt install -y ffmpeg

# Ensure all necessary permissions
chmod +x start.sh

# Activate virtual environment (अगर कोई हो)
# source venv/bin/activate  

# Start the bot
python3 bot.py &  # Bot बैकग्राउंड में रन होगा
python3 healthcheck.py  # Health check सर्वर रन करेगा
