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
init(autoreset=True)


print(Fore.YELLOW + "Loading environment variables...")
load_dotenv()
print(Fore.GREEN + "Environment variables loaded successfully.")

def test_mongo_connection():
    try:
        print(Fore.YELLOW + "Initializing MongoUtil...")
        mongo_util = MongoUtil()
        print(Fore.GREEN + "MongoUtil initialized successfully.")
        
        print(Fore.YELLOW + "Retrieving MongoDB URI...")
        mongo_uri = mongo_util.mongo_uri
        if mongo_uri:
            print(Fore.GREEN + f"MongoDB URI retrieved: {mongo_uri}")
        else:
            print(Fore.RED + "MongoDB URI not found. Please check your environment variables.")
            return
        
        print(Fore.YELLOW + "Connecting to MongoDB...")
        db = mongo_util.db
        print(Fore.GREEN + "Connection to MongoDB established.")
        
        print(Fore.YELLOW + "Listing collections in the database...")
        collections = db.list_collection_names()
        if collections:
            print(Fore.GREEN + f"Collections found: {collections}")
        else:
            print(Fore.RED + "No collections found in the database.")
        
        print(Fore.CYAN + "Connection to MongoDB successful!")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
        print(Fore.RED + "Debugging tips:")
        print(Fore.RED + "- Check if MongoDB is running.")
        print(Fore.RED + "- Ensure your environment variables are set correctly.")
        print(Fore.RED + "- Verify your network connection.")
        print(Fore.RED + "- Look for any typos in your MongoDB URI or credentials.")

if __name__ == "__main__":
    print(Fore.CYAN + "Starting MongoDB connection test...")
    test_mongo_connection()
    print(Fore.CYAN + "MongoDB connection test finished.")
