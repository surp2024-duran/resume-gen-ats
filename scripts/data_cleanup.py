# To connect to drive when using colab
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import re

def filter_by_keywords(df, column_name, keywords):
    keywords_lower = [keyword.lower() for keyword in keywords]
    return df[df[column_name].str.lower().str.contains('|'.join(keywords_lower), case=False, na=False)]

def clean_text(text):
  text=text.strip()
  text = re.sub(r'\s+', ' ', text)
  return text

def clean_and_save_data(file_paths, keywords, output_dir):
    # Initialize dictionary to store filtered dataframes
    filtered_dataframes = {}

    # Loop through the file paths
    for key, path in file_paths.items():
        # Load data
        df = pd.read_csv(path)

        if key == "resumes":
            # Drop rows with missing values in 'Text'
            df = df.dropna(subset=['Text'])
            # Limit to random 1000 samples
            df = df.sample(n=1000, random_state=1)
            # Keep only the 'Text' column
            df = df[['Text']]
        elif key == "job_postings":
            # Filter job postings based on the keywords
            df = filter_by_keywords(df, 'title', keywords)
            # Drop rows with missing values in 'description'
            df = df.dropna(subset=['description'])
            df['description']=df['description'].apply(clean_text)
            df = df[df['description'].str.len() > 10]
            df = df.sample(n=1000, random_state=1)
            # Keep only the 'description' column
            df = df[['description']]

        # Store the cleaned dataframe
        filtered_dataframes[key] = df

        # Save the cleaned and limited data to new CSV files
        output_path = f"{output_dir}/cleaned_{key}.csv"
        df.to_csv(output_path, index=False)
        print(f"{key.capitalize()} data cleaned and saved to {output_path}")

    print("Data cleanup completed for all files.")
    return filtered_dataframes

if __name__ == "__main__":
    # File paths from colab and keywords
    file_paths = {
        "resumes": "/content/drive//My Drive/SURP Data 2024/dataset_entities.csv",
        "job_postings": "/content/drive//My Drive/SURP Data 2024/postings.csv"
    }
    keywords = ["software engineer", "machine learning", "data scientist", "python", "java", "programming", "backend", "frontend", "developer"]
    output_dir = "/content/drive/My Drive/SURP Data 2024"  # Output directory

    # Clean and save data
    clean_and_save_data(file_paths, keywords, output_dir)