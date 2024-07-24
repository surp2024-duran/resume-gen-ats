import os
import time
import sys
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from colorama import init, Fore, Style
import certifi
import pytz

init()

load_dotenv()

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL, end='\n'):
    print(f"{style}{color}{text}{Style.RESET_ALL}", end=end)

def get_mongo_client():
    print_colored("Connecting to MongoDB...", Fore.CYAN)
    mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_URI')}"
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
            {
                "claiming": {"$exists": False},
                "didBy": {"$exists": False}
            },
            {"$set": {"claiming": True}},
            sort=[('_id', 1)],
            return_document=ReturnDocument.AFTER
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

def update_documents(collection, document_id, update_data):
    print_colored("Updating document...", Fore.CYAN)
    try:
        result = collection.update_one(
            {"_id": ObjectId(document_id)},
            {
                "$set": update_data,
                "$unset": {"claiming": ""},
                "$rename": {"editedBy": "didBy"}
            }
        )
        if result.modified_count > 0:
            print_colored(f"Successfully updated document with ID: {document_id}.", Fore.GREEN)
        else:
            print_colored("No document was updated. The document may already have the same values.", Fore.YELLOW)
    except Exception as e:
        print_colored(f"Error updating document: {e}", Fore.RED)

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

def display_paginated_text(text, title):
    print_colored(f"\n{title}:", Fore.CYAN, Style.BRIGHT)
    lines = text.split('\n')
    page_size = 10
    for i in range(0, len(lines), page_size):
        print_colored('\n'.join(lines[i:i+page_size]), Fore.WHITE)
        if i + page_size < len(lines):
            input("Press Enter to continue...")

def display_document(document):
    print_colored("\n" + "="*50, Fore.CYAN)
    print_colored(f"Current Document ID: {document['_id']}", Fore.GREEN, Style.BRIGHT)
    display_paginated_text(document.get('resume_text', 'N/A'), "Resume Text")
    display_paginated_text(document.get('job_descriptions', 'N/A'), "Job Description")
    display_paginated_text(document.get('generated_resume', 'N/A'), "Generated Resume")
    print_colored("="*50 + "\n", Fore.CYAN)

def edit_document(collection, document):
    while True:
        print_colored("\nEdit Menu:", Fore.CYAN)
        print_colored("1. Edit Score", Fore.WHITE)
        print_colored("2. Edit Truthfulness", Fore.WHITE)
        print_colored("3. Save and Exit", Fore.WHITE)
        choice = get_user_input("Enter your choice (1-3): ", 'int', range(1, 4))

        if choice == 1:
            score = get_user_input("Enter the new score for this document (0-100): ", 'int', range(101))
            document['score'] = score
        elif choice == 2:
            truthfulness = get_user_input("Is this document truthful? (yes/no): ", 'bool')
            document['truthfulness'] = truthfulness
        elif choice == 3:
            update_data = {
                "score": document.get('score'),
                "truthfulness": document.get('truthfulness'),
                "editedBy": document.get('editedBy')
            }
            update_documents(collection, document['_id'], update_data)
            break

def main():
    client = get_mongo_client()
    if not client:
        print_colored("Failed to connect to MongoDB. Exiting script.", Fore.RED)
        return

    db = client[os.getenv('MONGO_DB_NAME')]
    timezone = pytz.timezone(os.getenv("PYTZ_TIMEZONE"))
    current_date = datetime.now(timezone).strftime('%B-%d').lower()
    resumes_collection_name = f"{current_date}-resumes"
    resumes_collection = db[resumes_collection_name]

    print_colored(f"Connected to database: {os.getenv('MONGO_DB_NAME')}", Fore.GREEN)
    print_colored(f"Using collection: {resumes_collection_name}", Fore.GREEN)

    print_colored("\nWelcome to the Resume Evaluation System!", Fore.CYAN, Style.BRIGHT)
    print_colored("You can type 'quit' at any time to safely exit the script.", Fore.YELLOW)
    
    volunteer_name = get_user_input("Please enter your name: ", 'str')
    print_colored(f"Thank you, {volunteer_name}! Let's begin evaluating resumes.", Fore.GREEN)

    while True:
        document = find_and_claim_document(resumes_collection)
        if not document:
            print_colored("No more documents to update. Exiting script.", Fore.YELLOW)
            break

        display_document(document)

        score = get_user_input("Enter the score for this document (0-100): ", 'int', range(101))
        truthfulness = get_user_input("Is this document truthful? (yes/no): ", 'bool')

        document['score'] = score
        document['truthfulness'] = truthfulness
        document['editedBy'] = volunteer_name

        print_colored("\nSummary of your evaluation:", Fore.CYAN)
        print_colored(f"Score: {score}", Fore.WHITE)
        print_colored(f"Truthfulness: {truthfulness}", Fore.WHITE)

        confirm = get_user_input("Do you want to save this evaluation? (yes/no): ", 'bool')
        if confirm:
            update_data = {
                "score": score,
                "truthfulness": truthfulness,
                "editedBy": volunteer_name
            }
            update_documents(resumes_collection, document['_id'], update_data)
        else:
            edit_document(resumes_collection, document)

        print_colored("\nDocument processing complete.", Fore.GREEN)
        time.sleep(1)

        user_continue = get_user_input("Do you want to process another document? (yes/no): ", 'bool')
        if not user_continue:
            print_colored("Exiting the script. Thank you for your contributions!", Fore.YELLOW)
            break

    print_colored("All changes completed. Closing database connection.", Fore.GREEN)
    client.close()

if __name__ == "__main__":
    main()