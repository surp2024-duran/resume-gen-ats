# util/mongo_util.py
# util/mongo_util.py
import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
from dotenv import load_dotenv
import pytz

load_dotenv()

class MongoUtil:
    def __init__(self):
        self.mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_URI')}"
        self.client = MongoClient(self.mongo_uri, tlsCAFile=certifi.where())
        self.db = self.client[os.getenv('MONGO_DB_NAME')]
        #self.pst = pytz.timezone('US/Eastern')
        self.pst = pytz.timezone(os.getenv('PYTZ_TIMEZONE'))

    def get_previous_day_collection(self):
        previous_day = datetime.now(self.pst) - timedelta(days=1)
        collection_name = previous_day.strftime('%B-%d-resumes').lower()
        return self.db[collection_name]

    def get_today_collection_name(self):
        today = datetime.now(self.pst)
        return today.strftime('%B-%d-resumes').lower()

    def get_or_create_collection(self, collection_name):
        if collection_name not in self.db.list_collection_names():
            print(f"Creating collection: {collection_name}")
        return self.db[collection_name]

    def fetch_documents(self, collection):
        return list(collection.find({}))

    def insert_document(self, collection, document):
        collection.insert_one(document)

    def close_connection(self):
        self.client.close()