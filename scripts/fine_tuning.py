# scripts/fine_tuning.py
import os
import pandas as pd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm
import time
from sklearn.model_selection import train_test_split
from pymongo import MongoClient
import json


load_dotenv()


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


mongo_client = MongoClient(f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_URI')}")
db = mongo_client[os.getenv('MONGO_DB_NAME')]
collection = db[os.getenv('MONGO_COLLECTION_EDITED_NAME')]

def load_data():
    print("Loading data...")
    resumes = pd.read_csv('data/output/reduced_resumes.csv')
    postings = pd.read_csv('data/output/reduced_postings.csv')
    post_edit = pd.read_csv('data/output/reduced_resumes_post_edit.csv')
    print(f"Loaded {len(resumes)} resumes, {len(postings)} job postings, and {len(post_edit)} post-edit records.")
    return resumes, postings, post_edit

def prepare_fine_tuning_data(post_edit):
    print("Preparing fine-tuning data...")
    fine_tuning_data = []
    for _, row in tqdm(post_edit.iterrows(), total=len(post_edit), desc="Preparing data"):
        messages = [
            {"role": "system", "content": "You are an AI assistant that optimizes resumes for job applications."},
            {"role": "user", "content": f"Original Resume: {row['resume_text']}\n\nJob Description: {row['job_description']}"},
            {"role": "assistant", "content": row['generated_resume']}
        ]
        fine_tuning_data.append({"messages": messages})
    return fine_tuning_data

def create_fine_tuning_file(data):
    print("Creating fine-tuning file...")
    file_path = "fine_tuning_data.jsonl"
    with open(file_path, 'w') as f:
        for item in data:
            json.dump(item, f)
            f.write('\n')
    return file_path

def upload_fine_tuning_file(file_path):
    print("Uploading fine-tuning file...")
    with open(file_path, 'rb') as f:
        response = client.files.create(file=f, purpose="fine-tune")
    return response.id

def create_fine_tuning_job(file_id):
    print("Creating fine-tuning job...")
    response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo-0125"
    )
    return response.id

def monitor_fine_tuning_job(job_id):
    print(f"Monitoring fine-tuning job {job_id}...")
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        print(f"Job status: {job.status}")
        if job.status in ['succeeded', 'failed']:
            break
        time.sleep(60)  
    return job

def evaluate_model(model_id, test_data):
    print(f"Evaluating model {model_id}...")
    total_score = 0
    for item in tqdm(test_data, desc="Evaluating"):
        prompt = f"Original Resume: {item['resume_text']}\n\nJob Description: {item['job_description']}"
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are an AI assistant that optimizes resumes for job applications."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_resume = response.choices[0].message.content
        
        
        similarity = len(set(generated_resume.split()) & set(item['generated_resume'].split())) / len(set(item['generated_resume'].split()))
        total_score += similarity
    average_score = total_score / len(test_data)
    print(f"Average evaluation score: {average_score}")
    return average_score

def main():
    print("Starting fine-tuning process...")
    resumes, postings, post_edit = load_data()
    
    
    fine_tuning_data = prepare_fine_tuning_data(post_edit)
    
    
    train_data, test_data = train_test_split(fine_tuning_data, test_size=0.2, random_state=42)
    
    
    file_path = create_fine_tuning_file(train_data)
    file_id = upload_fine_tuning_file(file_path)
    
    
    job_id = create_fine_tuning_job(file_id)
    job = monitor_fine_tuning_job(job_id)
    
    if job.status == 'succeeded':
        print(f"Fine-tuning completed successfully. Model ID: {job.fine_tuned_model}")
        
        
        evaluation_score = evaluate_model(job.fine_tuned_model, test_data)
        
        
        result = {
            "model_id": job.fine_tuned_model,
            "evaluation_score": evaluation_score,
            "timestamp": time.time()
        }
        collection.insert_one(result)
        print("Results stored in MongoDB.")
    else:
        print("Fine-tuning job failed.")

if __name__ == "__main__":
    main()