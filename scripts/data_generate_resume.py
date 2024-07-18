import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
import argparse
from tqdm import tqdm
import time

load_dotenv()

def generate_optimized_resume(client, resume, job_description):
    prompt = (
        f"Given the following resume:\n\n{resume}\n\n"
        f"and the job description:\n\n{job_description}\n\n"
        "Generate an optimized resume to better fit the job description."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in optimizing resumes."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content, prompt
    except Exception as e:
        print(f"An error occurred while generating the optimized resume: {e}")
        return None, None

def main(num_resumes=None):
    print("Initializing OpenAI client...")
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("Reading processed data...")
    resumes_df = pd.read_csv('data/processed/cleaned_resumes.csv')
    job_postings_df = pd.read_csv('data/processed/cleaned_job_postings.csv')
    
    print(f"Resume count: {len(resumes_df)}")
    print(f"Job posting count: {len(job_postings_df)}")
    
    # Ensure we have an equal number of resumes and job postings
    min_count = min(len(resumes_df), len(job_postings_df))
    if num_resumes:
        min_count = min(min_count, num_resumes)
    
    resumes_df = resumes_df.head(min_count)
    job_postings_df = job_postings_df.head(min_count)
    
    print(f"Processing {min_count} resume-job pairs...")
    
    results = []
    start_time = time.time()
    
    with tqdm(total=min_count, desc="Generating Resumes", unit="pair") as pbar:
        for (_, resume_row), (_, job_row) in zip(resumes_df.iterrows(), job_postings_df.iterrows()):
            generated_resume, prompt = generate_optimized_resume(client, resume_row['resume_text'], job_row['job_description'])
            if generated_resume:
                results.append({
                    'resume_text': resume_row['resume_text'],
                    'job_description': job_row['job_description'],
                    'generated_resume': generated_resume,
                    'prompt': prompt
                })
            pbar.update(1)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\nGenerated {len(results)} optimized resumes.")
    print(f"Total time taken: {elapsed_time:.2f} seconds")
    print(f"Average time per resume: {elapsed_time/len(results):.2f} seconds")
    
    output_df = pd.DataFrame(results)
    os.makedirs('data/output', exist_ok=True)
    output_path = 'data/output/resumes_post_edit.csv'
    output_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate optimized resumes")
    parser.add_argument("--num_resumes", type=int, help="Number of resumes to process (default: all)")
    args = parser.parse_args()
    
    main(num_resumes=args.num_resumes)