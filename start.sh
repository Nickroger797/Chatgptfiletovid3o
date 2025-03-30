#!/bin/bash

echo "✅ Starting Video Converter Bot..."

# Flask Health Check Server बैकग्राउंड में चलाओ
python3 healthcheck.py &  

# Telegram Bot स्टार्ट करो
python3 bot.py
