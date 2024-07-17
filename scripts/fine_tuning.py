from pymongo import MongoClient
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client():
    mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_URI')}"
    return MongoClient(mongo_uri)

def prepare_training_data(collection):
    training_data = []
    for doc in collection.find({'score': {'$exists': True}, 'truthfulness': {'$exists': True}}):
        training_data.append({
            "messages": [
                {"role": "system", "content": "You are an AI assistant that optimizes resumes."},
                {"role": "user", "content": doc['prompt']},
                {"role": "assistant", "content": doc['generated_resume']},
                {"role": "human", "content": f"Score: {doc['score']}, Truthfulness: {doc['truthfulness']}"}
            ]
        })
    return training_data

def fine_tune_model(client, training_data):
    try:
        file = client.files.create(
            file=training_data,
            purpose='fine-tune'
        )
        fine_tuning_job = client.fine_tuning.jobs.create(
            training_file=file.id,
            model="gpt-3.5-turbo-0125"
        )
        return fine_tuning_job
    except Exception as e:
        print(f"An error occurred during fine-tuning: {e}")
        return None

def main():
    mongo_client = get_mongo_client()
    db = mongo_client[os.getenv('MONGO_DB_NAME')]
    collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]

    training_data = prepare_training_data(collection)
    
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    if training_data:
        job = fine_tune_model(openai_client, training_data)
        if job:
            print(f"Fine-tuning job created with ID: {job.id}")
    else:
        print("No suitable training data found.")

if __name__ == "__main__":
    main()