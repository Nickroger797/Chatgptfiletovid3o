#!/bin/bash

# Ensure all necessary permissions
chmod +x start.sh

# Activate virtual environment (अगर कोई हो)
# source venv/bin/activate  

python3 bot.py &  # Bot बैकग्राउंड में रन होगा
python3 healthcheck.py  # Health check सर्वर रन करेगा
