import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from tqdm import tqdm
import time
import urllib.parse
import certifi

load_dotenv()

def get_mongo_client():
    print("Connecting to MongoDB...")
    username = urllib.parse.quote_plus(os.getenv('MONGO_USERNAME_TEST'))
    password = urllib.parse.quote_plus(os.getenv('MONGO_PASSWORD_TEST'))
    cluster = os.getenv('MONGO_URI')
    db_name = os.getenv('MONGO_DB_NAME')
    
    mongo_uri = f"mongodb+srv://{username}:{password}@{cluster}/{db_name}?retryWrites=true&w=majority"
    
    return MongoClient(mongo_uri, tlsCAFile=certifi.where())


def upload_to_mongodb(collection, records):
    print(f"Uploading {len(records)} records to MongoDB...")
    start_time = time.time()
    
    for record in tqdm(records, desc="Uploading", unit="record"):
        try:
            collection.insert_one(record)
        except Exception as e:
            print(f"Error uploading record: {e}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Upload completed in {elapsed_time:.2f} seconds")
    print(f"Average time per record: {elapsed_time/len(records):.4f} seconds")

def main():
    print("Starting data upload process...")
    
    client = get_mongo_client()

    try:
        db_name = os.getenv('MONGO_DB_NAME')
        collection_name = os.getenv('MONGO_COLLECTION_NAME')
        
        print(f"Connecting to database: {db_name}")
        db = client[db_name]
        
        print(f"Accessing collection: {collection_name}")
        collection = db[collection_name]
        
        input_file = 'data/output/resumes_post_edit.csv'
        print(f"Reading data from {input_file}...")
        
        df = pd.read_csv(input_file)
        print(f"Successfully read {len(df)} records from {input_file}")
        
        print("Converting DataFrame to list of dictionaries...")
        records = df.to_dict('records')
        
        upload_to_mongodb(collection, records)
        
        print("Checking total documents in the collection...")
        total_docs = collection.count_documents({})
        print(f"Total documents in {collection_name} after upload: {total_docs}")
        
    except Exception as e:
        print(f"An error occurred during the upload process: {e}")
    
    finally:
        if client:
            client.close()
            print("MongoDB connection closed.")
    
    print("Data upload process completed.")

if __name__ == "__main__":
    main()