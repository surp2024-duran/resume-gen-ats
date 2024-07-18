# scripts/data_cleanup.py
import boto3
import pandas as pd
import os
import re
from dotenv import load_dotenv
from tqdm import tqdm
import time

load_dotenv()

def get_s3_client():
    print("Initializing S3 client...")
    return boto3.client('s3',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def read_csv_from_s3(bucket, key):
    print(f"Reading {key} from S3 bucket {bucket}...")
    s3_client = get_s3_client()
    response = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(response['Body'])
    print(f"Successfully read {key}. Shape: {df.shape}")
    return df

def filter_by_keywords(df, column_name, keywords):
    print(f"Filtering {column_name} by keywords: {keywords}")
    keywords_lower = [keyword.lower() for keyword in keywords]
    filtered_df = df[df[column_name].str.lower().str.contains('|'.join(keywords_lower), case=False, na=False)]
    print(f"Filtered shape: {filtered_df.shape}")
    return filtered_df

def clean_text(text):
    if pd.isna(text):
        return text
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def clean_and_save_data(file_paths, keywords, input_dir, output_dir):
    for key, path in file_paths.items():
        print(f"\nProcessing {key} data...")
        start_time = time.time()
        
        df = read_csv_from_s3(os.getenv('S3_BUCKET'), path)
        
        # Save raw data
        raw_path = os.path.join(input_dir, f"{key}.csv")
        df.to_csv(raw_path, index=False)
        print(f"Saved raw {key} data to {raw_path}")
        
        if key == "resumes":
            print("Cleaning resumes data...")
            df = df.dropna(subset=['Text'])
            print(f"Shape after dropping NA: {df.shape}")
            df = df.sample(n=min(1000, len(df)), random_state=1)
            print(f"Shape after sampling: {df.shape}")
            df = df[['Text']]
            df = df.rename(columns={'Text': 'resume_text'})
        elif key == "job_postings":
            print("Cleaning job postings data...")
            df = filter_by_keywords(df, 'title', keywords)
            df = df.dropna(subset=['description'])
            print(f"Shape after dropping NA: {df.shape}")
            print("Cleaning description text...")
            tqdm.pandas(desc="Cleaning text")
            df['description'] = df['description'].progress_apply(clean_text)
            df = df[df['description'].str.len() > 10]
            print(f"Shape after filtering short descriptions: {df.shape}")
            df = df.sample(n=min(1000, len(df)), random_state=1)
            print(f"Shape after sampling: {df.shape}")
            df = df[['description']]
            df = df.rename(columns={'description': 'job_description'})
        
        cleaned_path = os.path.join(output_dir, f"cleaned_{key}.csv")
        df.to_csv(cleaned_path, index=False)
        print(f"Saved cleaned {key} data to {cleaned_path}")
        
        end_time = time.time()
        print(f"Time taken to process {key}: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    print("Starting data cleanup process...")
    start_time = time.time()
    
    file_paths = {
        "resumes": "resumes.csv",
        "job_postings": "postings.csv"
    }
    keywords = ["software engineer", "machine learning", "data scientist", "python", "java", "programming", "backend", "frontend", "developer"]
    input_dir = "data/input"
    output_dir = "data/processed"
    
    print(f"Creating directories: {input_dir} and {output_dir}")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    clean_and_save_data(file_paths, keywords, input_dir, output_dir)
    
    end_time = time.time()
    print(f"Data cleanup process completed in {end_time - start_time:.2f} seconds.")