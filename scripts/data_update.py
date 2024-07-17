from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client():
    mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_URI')}"
    return MongoClient(mongo_uri)

def update_documents(collection, query, update):
    try:
        result = collection.update_one(query, update)
        if result.modified_count > 0:
            print(f"{result.modified_count} document(s) updated successfully.")
        else:
            print("No document was updated.")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_document_by_id(collection, document_id):
    try:
        return collection.find_one({"_id": ObjectId(document_id)})
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    client = get_mongo_client()
    db = client[os.getenv('MONGO_DB_NAME')]
    resumes_collection = db[os.getenv('MONGO_COLLECTION_NAME')]
    post_edit_collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]

    while True:
        document_id = input("Enter the document ID to update (or 'exit' to quit): ").strip()
        if document_id.lower() == 'exit':
            break
        
        document = find_document_by_id(resumes_collection, document_id)
        if document:
            print(f"\nCurrent Document: {document}")
            user_input_score = input("Enter the score for this document: ")
            user_input_truth = input("Enter the truthfulness for this document (True/False): ")
            try:
                score = int(user_input_score)
                truthfulness = user_input_truth.lower() in ['true', 't']
                update_data = {"$set": {"score": score, "truthfulness": truthfulness}}
                update_documents(resumes_collection, {"_id": ObjectId(document_id)}, update_data)
                
                # Copy updated document to Resumes_Post_Edit collection
                document.update({"score": score, "truthfulness": truthfulness})
                post_edit_collection.insert_one(document)
                print("Document copied to Resumes_Post_Edit collection.")
            except ValueError:
                print("Invalid input.")
        else:
            print("Document not found.")

if __name__ == "__main__":
    main()