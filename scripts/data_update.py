# scripts/data_update.pyx``
import os
import time
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from colorama import init, Fore, Style
import certifi

init()

load_dotenv()

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL, end='\n'):
    print(f"{style}{color}{text}{Style.RESET_ALL}", end=end)

def get_mongo_client():
    print_colored("Connecting to MongoDB...", Fore.CYAN)
    mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME_TEST')}:{os.getenv('MONGO_PASSWORD_TEST')}@{os.getenv('MONGO_URI')}"
    try:
        client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
        print_colored("Successfully connected to MongoDB.", Fore.GREEN)
        return client
    except Exception as e:
        print_colored(f"Error connecting to MongoDB: {e}", Fore.RED)
        return None

def find_and_claim_document(collection):
    print_colored("Searching for an unclaimed document...", Fore.CYAN)
    try:
        document = collection.find_one_and_update(
            {"$and": [{"claiming": {"$exists": False}}, {"$or": [{"score": {"$exists": False}}, {"truthfulness": {"$exists": False}}]}]},
            {"$set": {"claiming": True}},
            sort=[('_id', 1)],
            return_document=True
        )
        if document:
            print_colored(f"Found and claimed document with ID: {document['_id']}", Fore.GREEN)
        else:
            print_colored("No unclaimed documents found.", Fore.YELLOW)
        return document
    except Exception as e:
        print_colored(f"Error while finding and claiming document: {e}", Fore.RED)
        return None

def reset_claiming_status(collection, document_id):
    print_colored(f"Resetting claiming status for document {document_id}...", Fore.CYAN)
    try:
        result = collection.update_one({"_id": ObjectId(document_id)}, {"$unset": {"claiming": ""}})
        if result.modified_count > 0:
            print_colored(f"Successfully reset claiming status for document {document_id}", Fore.GREEN)
        else:
            print_colored(f"No changes made to document {document_id}", Fore.YELLOW)
    except Exception as e:
        print_colored(f"Error resetting claiming status: {e}", Fore.RED)

def update_documents(collection, query, update):
    print_colored("Updating document...", Fore.CYAN)
    try:
        result = collection.update_one(query, update)
        if result.modified_count > 0:
            print_colored(f"Successfully updated {result.modified_count} document(s).", Fore.GREEN)
        else:
            print_colored("No document was updated. The document may already have the same values.", Fore.YELLOW)
    except Exception as e:
        print_colored(f"Error updating document: {e}", Fore.RED)

def insert_document(collection, document):
    print_colored("Inserting document into post-edit collection...", Fore.CYAN)
    try:
        result = collection.insert_one(document)
        if result.inserted_id:
            print_colored(f"Document successfully inserted with ID: {result.inserted_id}", Fore.GREEN)
            return result.inserted_id
        else:
            print_colored("Document insertion failed.", Fore.RED)
            return None
    except Exception as e:
        print_colored(f"Error inserting document: {e}", Fore.RED)
        return None

def get_user_input(prompt, input_type, valid_range=None):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'quit':
            print_colored("Exiting the script. Thank you for your contributions!", Fore.YELLOW)
            sys.exit(0)
        
        if input_type == 'int':
            try:
                value = int(user_input)
                if valid_range and value not in valid_range:
                    print_colored(f"Error: Value must be between {valid_range.start} and {valid_range.stop-1}. Please try again.", Fore.RED)
                else:
                    return value
            except ValueError:
                print_colored("Error: Invalid input. Please enter a number.", Fore.RED)
        elif input_type == 'bool':
            if user_input in ['yes', 'y', 'true', 't']:
                return True
            elif user_input in ['no', 'n', 'false', 'f']:
                return False
            else:
                print_colored("Error: Invalid input. Please enter 'yes' or 'no'.", Fore.RED)
        else:
            return user_input

def main():
    client = get_mongo_client()
    if not client:
        print_colored("Failed to connect to MongoDB. Exiting script.", Fore.RED)
        return

    db = client[os.getenv('MONGO_DB_NAME')]
    resumes_collection = db[os.getenv('MONGO_COLLECTION_NAME')]
    post_edit_collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]

    print_colored(f"Connected to database: {os.getenv('MONGO_DB_NAME')}", Fore.GREEN)
    print_colored(f"Using collections: {os.getenv('MONGO_COLLECTION_NAME')} and {os.getenv('MONGO_COLLECTION_EDITED_NAME')}", Fore.GREEN)

    print_colored("\nWelcome to the Resume Evaluation System!", Fore.CYAN, Style.BRIGHT)
    print_colored("You can type 'quit' at any time to safely exit the script.", Fore.YELLOW)
    
    volunteer_name = get_user_input("Please enter your name: ", 'str')
    print_colored(f"Thank you, {volunteer_name}! Let's begin evaluating resumes.", Fore.GREEN)

    while True:
        document = find_and_claim_document(resumes_collection)
        if not document:
            print_colored("No more documents to update. Exiting script.", Fore.YELLOW)
            break

        document_id = document['_id']
        score_exists = 'score' in document and document['score'] is not None
        truthfulness_exists = 'truthfulness' in document and document['truthfulness'] is not None

        if score_exists and truthfulness_exists:
            print_colored(f"\nDocument {document_id} is already filled:", Fore.YELLOW)
            print_colored(f"Score: {document['score']}", Fore.CYAN)
            print_colored(f"Truthfulness: {document['truthfulness']}", Fore.CYAN)
            reset_claiming_status(resumes_collection, document_id)
            continue

        print_colored("\n" + "="*50, Fore.CYAN)
        print_colored(f"Current Document ID: {document_id}", Fore.GREEN, Style.BRIGHT)
        print_colored(f"Resume Text: {document.get('resume_text', 'N/A')[:100]}...", Fore.WHITE)
        print_colored(f"Job Description: {document.get('job_descriptions', 'N/A')[:100]}...", Fore.WHITE)
        print_colored(f"Generated Resume: {document.get('generated_resume', 'N/A')[:100]}...", Fore.WHITE)
        print_colored("="*50 + "\n", Fore.CYAN)

        score = get_user_input("Enter the score for this document (0-100): ", 'int', range(101))
        truthfulness = get_user_input("Is this document truthful? (yes/no): ", 'bool')

        update_data = {
            "$set": {
                "score": score, 
                "truthfulness": truthfulness, 
                "editedBy": volunteer_name
            }, 
            "$unset": {"claiming": ""}
        }
        update_documents(resumes_collection, {"_id": ObjectId(document_id)}, update_data)

        document.update({"score": score, "truthfulness": truthfulness, "editedBy": volunteer_name})
        insert_document(post_edit_collection, document)

        print_colored("\nDocument processing complete.", Fore.GREEN)
        time.sleep(1)  # Short pause for readability

        user_continue = get_user_input("Do you want to process another document? (yes/no): ", 'bool')
        if not user_continue:
            print_colored("Exiting the script. Thank you for your contributions!", Fore.YELLOW)
            break

    print_colored("All changes completed. Closing database connection.", Fore.GREEN)
    client.close()

if __name__ == "__main__":
    main()