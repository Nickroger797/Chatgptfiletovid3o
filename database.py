from pymongo import MongoClient
from config import MONGO_URL
import logging

# ✅ MongoDB Connection
try:
    client = MongoClient(MONGO_URL)
    db = client["video_converter"]
    users_col = db["users"]
    logs_col = db["conversion_logs"]
    
    # ✅ Test connection
    client.server_info()  # Agar issue hoga toh exception raise karega
    logging.info("✅ MongoDB Connection Successful!")
except Exception as e:
    logging.error(f"❌ MongoDB Connection Failed: {e}")
    exit(1)  # ✅ Bina database ke bot run nahi hoga
