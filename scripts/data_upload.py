# scripts/data_upload.py
import os
from dotenv import load_dotenv
import pandas as pd
import json
from pymongo import MongoClient

load_dotenv()

def load_and_prepare_data(resumes_path, job_postings_path):
    limited_resumes = pd.read_csv(resumes_path)
    limited_job_postings = pd.read_csv(job_postings_path)
    limited_resumes['source'] = 'resume'
    limited_job_postings['source'] = 'job_posting'
    combined_df = pd.DataFrame({
        'resume_text': limited_resumes['Text'].tolist(),
        'job_description': limited_job_postings['description'].tolist()
    })
    return combined_df

def save_data_to_json(df, output_path):
    records = df.to_dict(orient='records')
    json_data = json.dumps(records, indent=4)
    with open(output_path, 'w') as json_file:
        json_file.write(json_data)
    print(f"Data saved to {output_path}")

def upload_to_mongodb(df):
    records = df.to_dict(orient='records')
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('MONGO_DB_NAME')]
    collection = db[os.getenv('MONGO_COLLECTION_NAME')]
    collection.insert_many(records)
    print("Data uploaded to MongoDB")

if __name__ == "__main__":
    resumes_path = 'data/processed/cleaned_resumes.csv'
    job_postings_path = 'data/processed/cleaned_job_postings.csv'
    json_output_path = 'data/output/cleaned_combined_data.json'

    combined_df = load_and_prepare_data(resumes_path, job_postings_path)
    save_data_to_json(combined_df, json_output_path)
    upload_to_mongodb(combined_df)