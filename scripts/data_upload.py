# Data upload
import pandas as pd
import json
from pymongo import MongoClient

def load_and_prepare_data(resumes_path, job_postings_path):
    # Read files
    limited_resumes = pd.read_csv(resumes_path)
    limited_job_postings = pd.read_csv(job_postings_path)

    limited_resumes['source'] = 'resume'
    limited_job_postings['source'] = 'job_posting'
    # Combine Resume and Job Listings
    combined_df = pd.DataFrame({
        'resume_text': limited_resumes['Text'].tolist(),
        'job_description': limited_job_postings['description'].tolist()
    })

    return combined_df

# Save to json file
def save_data_to_json(df, output_path):
    records = df.to_dict(orient='records')
    json_data = json.dumps(records, indent=4)
    with open(output_path, 'w') as json_file:
        json_file.write(json_data)
    print(f"Data saved to {output_path}")


# Connect to MongoDB
def upload_to_mongodb(df, uri, db_name, collection_name):
    records = df.to_dict(orient='records')
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(records)
    print("Data uploaded to MongoDB")

if __name__ == "__main__":
  # My path when using colab
    resumes_path = '/content/drive/My Drive/SURP Data 2024/cleaned_resumes.csv'
    job_postings_path = '/content/drive/My Drive/SURP Data 2024/cleaned_job_postings.csv'
    json_output_path = '/content/drive/My Drive/SURP Data 2024/cleaned_combined_data.json'
  # Credentials to connect to database
    uri = "mongodb+srv://Katie_He:FnloYEiSG59twAzF@surp24.rwhuwqq.mongodb.net/SURP24?retryWrites=true&w=majority"
    db_name = 'SURP24'
    collection_name = 'Resumes'

    combined_df = load_and_prepare_data(resumes_path, job_postings_path)
    save_data_to_json(combined_df, json_output_path)
    upload_to_mongodb(combined_df, uri, db_name, collection_name)