from pymongo import MongoClient
from app.config import get_settings

settings = get_settings()
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
jobs_collection = db[settings.MONGO_JOBS_COLLECTION]
