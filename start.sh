#!/bin/bash

echo "✅ Starting Video Converter Bot..."

# स्टार्ट.sh को एक्सीक्यूटेबल बनाओ (सिर्फ एक बार, अगर जरूरी हो)
chmod +x start.sh

# बॉट स्टार्ट करो
python3 bot.py
python3 healthcheck.py  # Health check सर्वर रन करेगा
