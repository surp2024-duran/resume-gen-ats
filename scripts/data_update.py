import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()

def get_mongo_client():
    mongo_uri = os.getenv('MONGO_URI')
    return MongoClient(mongo_uri)

def update_documents(query, update):
    try:
        client = get_mongo_client()
        db = client[os.getenv('MONGO_DB_NAME')]
        collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]
        result = collection.update_one(query, update)
        if result.modified_count > 0:
            print(f"{result.modified_count} document(s) updated successfully.")
        else:
            print("No document was updated.")
    except Exception as e:
        print(f"An error occurred: {e}")

def insert_document(document):
    try:
        client = get_mongo_client()
        db = client[os.getenv('MONGO_DB_NAME')]
        collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]
        result = collection.insert_one(document)
        if result.inserted_id:
            print(f"Document inserted successfully with _id: {result.inserted_id}")
            return result.inserted_id
        else:
            print("Document insertion failed.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def delete_document(query):
    try:
        client = get_mongo_client()
        db = client[os.getenv('MONGO_DB_NAME')]
        collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]
        result = collection.delete_one(query)
        if result.deleted_count > 0:
            print(f"{result.deleted_count} document(s) deleted successfully.")
        else:
            print("No document was deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_document_by_id(document_id):
    try:
        client = get_mongo_client()
        db = client[os.getenv('MONGO_DB_NAME')]
        collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]
        document = collection.find_one({"_id": ObjectId(document_id)})
        return document
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    while True:
        document_id = input("Enter the document ID to update (or 'exit' to quit): ").strip()
        if document_id.lower() == 'exit':
            break
        try:
            document_id = ObjectId(document_id)
            document = find_document_by_id(document_id)
            if document:
                print(f"\nCurrent Document: {document}")
                user_input_score = input("Enter the score for this document: ")
                user_input_truth = input("Enter the truthfulness for this document (True/False): ")
                try:
                    score = int(user_input_score)
                    truthfulness = user_input_truth.lower() in ['true', 't']
                    update_data = {"$set": {"score": score, "truthfulness": truthfulness}}
                    update_documents({"_id": document_id}, update_data)
                except ValueError:
                    print("Invalid input.")
            else:
                print("Document not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    print("Change Completed.")
