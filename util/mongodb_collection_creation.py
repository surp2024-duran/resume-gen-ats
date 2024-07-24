import os
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv

# this is to test whether i can make a mongodb collection from the cmd line 

load_dotenv()

def create_collection_in_db(db_name, new_collection_name):
    """
    Create a new collection in an existing MongoDB database.

    :param db_name: The name of the existing database.
    :param new_collection_name: The name of the new collection to create.
    """
    
    mongo_uri = os.getenv('MONGO_URI')
    mongo_username = os.getenv('MONGO_USERNAME')
    mongo_password = os.getenv('MONGO_PASSWORD')
    
    print(f"Using MongoDB URI: {mongo_uri}")
    print(f"Connecting to database '{db_name}' with user '{mongo_username}'")
    
    
    client = MongoClient(f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_uri}", tlsCAFile=certifi.where())
    db = client[db_name]
    
    
    existing_collections = db.list_collection_names()
    print(f"Existing collections in database '{db_name}': {existing_collections}")
    
    
    if new_collection_name in existing_collections:
        print(f"The collection '{new_collection_name}' already exists in the database '{db_name}'.")
    else:
        
        print(f"Creating collection '{new_collection_name}'...")
        db.create_collection(new_collection_name)
        print(f"The collection '{new_collection_name}' has been created in the database '{db_name}'.")
    
    
    print("Closing the MongoDB connection.")
    client.close()


if __name__ == "__main__":
    
    database_name = "SURP24"
    collection_name = "july-23-resumes"
    
    print(f"Attempting to create collection '{collection_name}' in database '{database_name}'...")
    
    create_collection_in_db(database_name, collection_name)
    print("Operation completed.")
