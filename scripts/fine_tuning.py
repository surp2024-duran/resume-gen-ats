import os
from dotenv import load_dotenv
from pymongo import MongoClient
from tqdm import tqdm
from openai import OpenAI
import json
import time
import random

load_dotenv()

def get_mongo_client():
    print("Connecting to MongoDB...")
    mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_URI')}"
    return MongoClient(mongo_uri)

def prepare_training_data(collection):
    print("Preparing training data...")
    training_data = []
    for doc in tqdm(collection.find({'score': {'$exists': True}, 'truthfulness': {'$exists': True}}), desc="Processing documents"):
        training_data.append({
            "messages": [
                {"role": "system", "content": "You are an AI assistant that optimizes resumes for high ATS scores."},
                {"role": "user", "content": f"Original resume:\n{doc['resume_text']}\nJob description:\n{doc['job_description']}"},
                {"role": "assistant", "content": doc['generated_resume']},
                {"role": "human", "content": f"Score: {doc['score']}, Truthfulness: {doc['truthfulness']}"}
            ]
        })
    print(f"Prepared {len(training_data)} training examples.")
    return training_data

def fine_tune_model(client, training_data):
    print("Starting fine-tuning process...")
    try:
        with open('training_data.jsonl', 'w') as f:
            for item in training_data:
                f.write(json.dumps(item) + '\n')

        file = client.files.create(
            file=open('training_data.jsonl', 'rb'),
            purpose="fine-tune"
        )
        print(f"Training file created with ID: {file.id}")

        job = client.fine_tuning.jobs.create(
            training_file=file.id,
            model="gpt-3.5-turbo-0125"
        )
        print(f"Fine-tuning job created with ID: {job.id}")

        # Monitor the fine-tuning job
        while True:
            job = client.fine_tuning.jobs.retrieve(job.id)
            print(f"Fine-tuning status: {job.status}")
            if job.status in ['succeeded', 'failed', 'cancelled']:
                break
            time.sleep(60)  # Check status every minute

        if job.status == 'succeeded':
            print(f"Fine-tuning completed successfully. New model: {job.fine_tuned_model}")
            return job.fine_tuned_model
        else:
            print(f"Fine-tuning failed with status: {job.status}")
            return None

    except Exception as e:
        print(f"An error occurred during fine-tuning: {e}")
        return None

def evaluate_model(client, model, test_data):
    print("Evaluating fine-tuned model...")
    total_score = 0
    for example in tqdm(test_data, desc="Evaluating examples"):
        prompt = f"Original resume:\n{example['resume_text']}\nJob description:\n{example['job_description']}"
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI assistant that optimizes resumes for high ATS scores."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_resume = response.choices[0].message.content
        
        # Here you would typically use EnhanCV to get a score, but for this example, we'll use a mock scoring function
        score = mock_enhancv_score(generated_resume, example['job_description'])
        total_score += score
    
    avg_score = total_score / len(test_data)
    print(f"Average EnhanCV score: {avg_score}")
    return avg_score

def mock_enhancv_score(resume, job_description):
    # This is a mock function to simulate EnhanCV scoring
    # In a real scenario, you would integrate with EnhanCV's API
    return random.uniform(60, 100)  # Returns a random score between 60 and 100

def main():
    print("Starting fine-tuning process...")
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    mongo_client = get_mongo_client()
    db = mongo_client[os.getenv('MONGO_DB_NAME')]
    collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]

    training_data = prepare_training_data(collection)
    
    if training_data:
        new_model = fine_tune_model(client, training_data)
        if new_model:
            # Split data for testing
            test_data = list(collection.find().limit(100))
            
            # Evaluate the new model
            new_model_score = evaluate_model(client, new_model, test_data)
            
            # Evaluate the old model for comparison
            old_model_score = evaluate_model(client, "gpt-3.5-turbo-0125", test_data)
            
            print(f"Old model average score: {old_model_score}")
            print(f"New model average score: {new_model_score}")
            
            if new_model_score > old_model_score:
                print("New model performs better. Updating default model...")
                # Here you would update your application to use the new model
            else:
                print("Old model still performs better. Keeping the old model.")
        else:
            print("Fine-tuning failed. Keeping the old model.")
    else:
        print("No suitable training data found.")

if __name__ == "__main__":
    main()