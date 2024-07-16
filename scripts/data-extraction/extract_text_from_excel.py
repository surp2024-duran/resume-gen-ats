import pandas as pd
import boto3
from io import StringIO

def extract_text_from_csv(s3_bucket, file_key):
    s3 = boto3.client('s3')
    
    # Download CSV file from S3
    response = s3.get_object(Bucket=s3_bucket, Key=file_key)
    csv_content = response['Body'].read().decode('utf-8')
    
    # Read CSV content
    df = pd.read_csv(StringIO(csv_content))
    
    # Extract text from relevant columns
    # Adjust column names as per your CSV structure
    extracted_text = df['text_column'].tolist()
    
    return extracted_text

if __name__ == "__main__":
    s3_bucket = "resume-gen-ats-raw-data"
    file_key = "resumes.csv"  # or "job_postings.csv"
    
    extracted_text = extract_text_from_csv(s3_bucket, file_key)
    print(f"Extracted {len(extracted_text)} text entries from {file_key}")