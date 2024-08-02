# scripts/fine_tuning.py

import os
import sys
import time
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
from util.mongo_util import MongoUtil
from datetime import datetime, timedelta
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)
from openai import APIConnectionError, APIError, RateLimitError

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

client = OpenAI(api_key=api_key)

@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
    retry=retry_if_exception_type((APIConnectionError, APIError, RateLimitError))
)
def generate_optimized_resume(resume_text, job_description):
    prompt = (
        "You are an AI resume optimizer. Your task is to create a highly optimized, ATS-friendly resume in LaTeX format based on the given original resume and job description. "
        "Follow these strict guidelines:\n\n"
        "1. Output ONLY the LaTeX code for the resume. Do not include any explanations, comments, or additional text.\n"
        "2. Use the following LaTeX structure:\n"
        "   \\documentclass[11pt,a4paper]{article}\n"
        "   \\usepackage[margin=1in]{geometry}\n"
        "   \\usepackage{titlesec}\n"
        "   \\usepackage{enumitem}\n"
        "   \\begin{document}\n"
        "   ... (resume content) ...\n"
        "   \\end{document}\n"
        "3. Include these sections in order: Education, Work Experience, Skills, and Certifications (if applicable).\n"
        "4. Use \\section{} for main headings and \\subsection{} for subheadings.\n"
        "5. Use itemize environments for bullet points.\n"
        "6. Incorporate relevant keywords from the job description naturally throughout the resume.\n"
        "7. Quantify achievements and responsibilities where possible.\n"
        "8. Ensure all information is truthful and accurately represents the original resume.\n"
        "9. Optimize the content for high ATS scores while maintaining readability.\n"
        "10. Do not include any personal contact information.\n\n"
        "Original Resume:\n"
        f"{resume_text}\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Generate the LaTeX resume now, starting with \\documentclass and ending with \\end{document}. Include ONLY the LaTeX code."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a LaTeX resume generator. Output only LaTeX code."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        generated_resume = response.choices[0].message.content.strip()
        return generated_resume, prompt
    except (APIConnectionError, APIError, RateLimitError) as e:
        print(f"An error occurred while generating the optimized resume: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

def fine_tune_and_store():
    result = {}
    print("Starting fine-tuning and storing process...")
    mongo_util = MongoUtil()
    
    today = datetime.now(mongo_util.pst)
    prev_day = today - timedelta(days=1)
    
    prev_collection_name = prev_day.strftime('%B-%d-resumes').lower()
    today_collection_name = today.strftime('%B-%d-resumes').lower()
    
    if today_collection_name in mongo_util.db.list_collection_names():
        print(f"Collection '{today_collection_name}' already exists. Stopping script execution.")
        result['status'] = 'stopped'
        result['reason'] = f"Collection '{today_collection_name}' already exists."
        with open('/tmp/fine_tuning_result.json', 'w') as f:
            json.dump(result, f)
        return

    prev_collection = mongo_util.db[prev_collection_name]
    today_collection = mongo_util.get_or_create_collection(today_collection_name)

    print(f"Fetching documents from previous day's collection: {prev_collection.name}")
    documents = mongo_util.fetch_documents(prev_collection)
    if not documents:
        print(f"No documents found in the previous day's collection.")
        result['status'] = 'no_documents'
        with open('/tmp/fine_tuning_result.json', 'w') as f:
            json.dump(result, f)
        return

    print(f"Processing {len(documents)} documents...")
    for doc in tqdm(documents, desc="Fine-tuning resumes", unit="resume"):
        resume_text = doc.get('resume_text', '')
        job_description = doc.get('job_description', '')
        try:
            generated_resume, prompt = generate_optimized_resume(resume_text, job_description)

            if generated_resume:
                new_doc = {
                    "resume_text": resume_text,
                    "job_description": job_description,
                    "generated_resume": generated_resume,
                    "prompt": prompt,
                    "original_id": doc['_id'],
                    "created_at": datetime.now(mongo_util.pst)  
                }
                mongo_util.insert_document(today_collection, new_doc)
                print(f"Stored new document in '{today_collection_name}' with original ID: {doc['_id']}")
            else:
                print(f"Failed to generate optimized resume for document with ID: {doc['_id']}")
        except Exception as e:
            print(f"Error processing document with ID: {doc['_id']}. Error: {e}")
            continue

        time.sleep(1)

    print(f"Completed fine-tuning and storing in the collection '{today_collection_name}'.")
    mongo_util.close_connection()
    print("Closed MongoDB connection. Process complete.")

    result['status'] = 'completed'
    result['collection'] = today_collection_name
    with open('/tmp/fine_tuning_result.json', 'w') as f:
        json.dump(result, f)

if __name__ == "__main__":
    print("Starting fine_tuning.py script...")
    try:
        fine_tune_and_store()
    except Exception as e:
        print(f"An error occurred during script execution: {e}")
    print("fine_tuning.py script execution completed.")