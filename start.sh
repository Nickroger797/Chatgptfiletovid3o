#!/bin/bash
chmod +x healthcheck.py
python3 bot.py &  # Bot बैकग्राउंड में रन होगा
python3 healthcheck.py  # Health check सर्वर रन करेगा
