import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests

load_dotenv()

def test_mongo_connection():
    try:
        mongo_uri = os.getenv("MONGO_FULL_URI")
        if not mongo_uri:
            raise ValueError("MONGO_FULL_URI is not set in the environment variables.")
        
        client = MongoClient(mongo_uri)
        db = client[os.getenv("MONGO_DB_NAME")]
        collections = db.list_collection_names()
        if collections:
            print(f"Successfully connected to MongoDB. Collections: {collections}")
        else:
            print("Connected to MongoDB but no collections found.")
        client.close()
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

def test_flask_endpoint():
    try:
        response = requests.get("http://127.0.0.1:5000/data")
        if response.status_code == 200:
            print("Successfully connected to Flask endpoint.")
        else:
            print(f"Failed to connect to Flask endpoint. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to Flask endpoint: {e}")

if __name__ == "__main__":
    print("Testing MongoDB connection...")
    test_mongo_connection()
    print("\nTesting Flask endpoint...")
    test_flask_endpoint()
