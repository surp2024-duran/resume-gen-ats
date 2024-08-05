# backend/app/models.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
mongo_uri = os.getenv('MONGO_FULL_URI')
mongo_db_name = os.getenv('MONGO_DB_NAME')
client = MongoClient(mongo_uri)
db = client[mongo_db_name]
