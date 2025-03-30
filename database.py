from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["video_converter"]
users_col = db["users"]
logs_col = db["conversion_logs"]
