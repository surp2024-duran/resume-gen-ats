# test_connect_string.py
import unittest
import sys
import os
from tqdm import tqdm
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.mongo_util import MongoUtil

load_dotenv()

def test_mongo_connection():
    try:
        mongo_util = MongoUtil()
        print(f"MongoDB URI: {mongo_util.mongo_uri}")
        db = mongo_util.db
        collections = db.list_collection_names()
        print(f"Collections: {collections}")

        print("Connection to MongoDB successful!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_mongo_connection()
