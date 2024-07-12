# Make sure to have pymongo installed (pip install pymongo)
from pymongo import MongoClient

# Update documents based on a query
def update_documents(query, update):
    try:

        # Connect to MongoDB client
        client = MongoClient(uri)   

        # Access the database and collection
        db = client[db_name]

        collection = db[collection_name]

        # Update the document based on query and update data
        result = collection.update_one(query, update)

        # Check if updated
        if result.modified_count > 0:
            print(f"{result.modified_count} document(s) updated successfully.")
        else:
            print("No document was updated.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Insert a document into the collection
def insert_document(document):
    try:
        client = MongoClient(uri)

        db = client[db_name]

        collection = db[collection_name]

        # Insert the document into the collection
        result = collection.insert_one(document)

        # Check if inserted
        if result.inserted_id:
            print(f"Document inserted successfully with _id: {result.inserted_id}")
            return result.inserted_id
        else:
            print("Document insertion failed.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Delete a document from the collection
def delete_document(query):
    try:
        client = MongoClient(uri)

        db = client[db_name]

        collection = db[collection_name]

        # Delete the document from collection
        result = collection.delete_one(query)

        # Check if deleted
        if result.deleted_count > 0:
            print(f"{result.deleted_count} document(s) deleted successfully.")
        else:
            print("No document was deleted.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Verify document existence
def find_document_by_id(document_id):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        # If documents id is found, the document exist
        document = collection.find_one({"_id": ObjectId(document_id)})
        return document

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    #replace the credentials with your own in the uri
    uri = 'mongodb+srv://Katie_He:FnloYEiSG59twAzF@surp24.rwhuwqq.mongodb.net/SURP24?retryWrites=true&w=majority'
    db_name = 'SURP24' #Same
    collection_name = 'Resumes' #Same

    while True:
      # Run the program
      # Find document with ID, if you want the loop to end, type exit
        document_id = input("Enter the document ID to update (or 'exit' to quit): ").strip()
        if document_id.lower() == 'exit':
            break
        try:
            document_id = ObjectId(document_id)
            document = find_document_by_id(document_id)
            if document:
              # Shows the current document
                print(f"\nCurrent Document: {document}")
                # Input ats score and truthfulness
                user_input_score = input("Enter the score for this document: ")
                user_input_truth = input("Enter the truthfulness for this document (True/False): ")
                try:
                    # Changes score to an integer
                    score = int(user_input_score)

                    # Ensures that the variation of truth still evaluates to True
                    truthfulness = user_input_truth.lower() in ['true', 't']
                    # Adds new columns and updates the score and truthfulness at the id you inputed
                    update_data = {"$set": {"score": score, "truthfulness": truthfulness}}
                    update_documents({"_id": document_id}, update_data)
                except ValueError:
                  # Score and truth input invalid
                    print("Invalid input.")
            else:
              # Document id cant be found
                print("Document not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    print("Change Completed.")