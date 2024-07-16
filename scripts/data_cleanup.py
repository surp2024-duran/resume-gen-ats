# scripts/data_cleanup.py
import os
from dotenv import load_dotenv
import pandas as pd
import re

load_dotenv()

def filter_by_keywords(df, column_name, keywords):
    keywords_lower = [keyword.lower() for keyword in keywords]
    return df[df[column_name].str.lower().str.contains('|'.join(keywords_lower), case=False, na=False)]

def clean_text(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def clean_and_save_data(file_paths, keywords, output_dir):
    filtered_dataframes = {}
    for key, path in file_paths.items():
        df = pd.read_csv(path)
        if key == "resumes":
            df = df.dropna(subset=['Text'])
            df = df.sample(n=1000, random_state=1)          
            df = df[['Text']]
        elif key == "job_postings":
            df = filter_by_keywords(df, 'title', keywords)  
            df = df.dropna(subset=['description'])
            df['description'] = df['description'].apply(clean_text)
            df = df[df['description'].str.len() > 10]
            df = df.sample(n=1000, random_state=1)    
            df = df[['description']]   
        filtered_dataframes[key] = df
        output_path = os.path.join(output_dir, f"cleaned_{key}.csv")
        df.to_csv(output_path, index=False)
        print(f"{key.capitalize()} data cleaned and saved to {output_path}")
    print("Data cleanup completed for all files.")
    return filtered_dataframes

if __name__ == "__main__":
    file_paths = {
        "resumes": "data/input/dataset_entities.csv",
        "job_postings": "data/input/postings.csv"
    }
    keywords = ["software engineer", "machine learning", "data scientist", "python", "java", "programming", "backend", "frontend", "developer"]
    output_dir = "data/processed"
    clean_and_save_data(file_paths, keywords, output_dir)