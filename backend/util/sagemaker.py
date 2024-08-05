import pandas as pd
import sys

def clean_csv_files(dataset_entities_path, postings_path, output_dataset_entities_path, output_postings_path):
    
    dataset_entities = pd.read_csv(dataset_entities_path)
    postings = pd.read_csv(postings_path)

    
    dataset_entities_columns = set(dataset_entities.columns)
    postings_columns = set(postings.columns)

    
    extra_in_dataset_entities = dataset_entities_columns - postings_columns
    extra_in_postings = postings_columns - dataset_entities_columns

    
    for col in extra_in_postings:
        if col in postings.columns:
            postings_dtype = postings[col].dtype
            if pd.api.types.is_numeric_dtype(postings_dtype):
                dataset_entities[col] = 0
            else:
                dataset_entities[col] = ""
        else:
            dataset_entities[col] = ""

    
    for col in extra_in_dataset_entities:
        if col in dataset_entities.columns:
            dataset_entities_dtype = dataset_entities[col].dtype
            if pd.api.types.is_numeric_dtype(dataset_entities_dtype):
                postings[col] = 0
            else:
                postings[col] = ""
        else:
            postings[col] = ""

    
    dataset_entities = dataset_entities[sorted(dataset_entities.columns)]
    postings = postings[sorted(postings.columns)]

    
    dataset_entities.to_csv(output_dataset_entities_path, index=False)
    postings.to_csv(output_postings_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python sagemaker.py <dataset_entities.csv> <postings.csv> <output_dataset_entities_cleaned.csv> <output_postings_cleaned.csv>")
    else:
        clean_csv_files(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
