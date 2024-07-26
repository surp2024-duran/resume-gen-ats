# scripts/fine_tuning.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
from util.mongo_util import MongoUtil
from datetime import datetime, timedelta
import json

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_optimized_resume(resume_text, job_description):
    print(f"Generating optimized resume for job description: {job_description[:100]}...")
    
    prompt = (
        "You are an expert AI assistant specializing in resume optimization for high ATS scores. "
        "Given the following resume and job description, generate a highly tailored and ATS-friendly resume. "
        "Focus on the following key aspects:\n"
        "1. Clear, concise structure with sections: 'Education', 'Work Experience', 'Skills', and 'Certifications'.\n"
        "2. Prioritize and prominently display the education section.\n"
        "3. Use bullet points for clarity and include specific dates where applicable.\n"
        "4. Incorporate relevant keywords from the job description naturally throughout the resume.\n"
        "5. Quantify achievements and responsibilities where possible.\n"
        "6. Ensure all information is truthful and accurately represents the original resume.\n"
        "7. Format the output in a clean, easy-to-read structure.\n\n"
        f"Original Resume:\n{resume_text}\n\n"
        f"Job Description:\n{job_description}\n\n"
        "Optimized Resume:"
    )
    
    try:
        print("Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume optimizer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        generated_resume = response.choices[0].message.content.strip()
        print(f"Successfully generated optimized resume. Length: {len(generated_resume)} characters.")
        return generated_resume, prompt
    except Exception as e:
        print(f"An error occurred while generating the optimized resume: {e}")
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

    print(f"Completed fine-tuning and storing in the collection '{today_collection_name}'.")
    mongo_util.close_connection()
    print("Closed MongoDB connection. Process complete.")

    result['status'] = 'completed'
    result['collection'] = today_collection_name
    with open('/tmp/fine_tuning_result.json', 'w') as f:
        json.dump(result, f)

if __name__ == "__main__":
    print("Starting fine_tuning.py script...")
    fine_tune_and_store()
    print("fine_tuning.py script execution completed.")