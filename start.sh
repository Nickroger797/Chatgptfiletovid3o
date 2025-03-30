#!/bin/bash
chmod +x healthcheck.py
chmod +x start.sh
git add start.sh
git commit -m "Make start.sh executable"
git push origin main  # या जो भी branch हो
python3 bot.py &  # Bot बैकग्राउंड में रन होगा
python3 healthcheck.py  # Health check सर्वर रन करेगा
