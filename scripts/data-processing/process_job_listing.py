import re

def clean_job_listing(text):
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_requirements(text):
    # Implement requirement extraction logic
    # This is a simplified example
    requirements = re.findall(r'(?:requires|must have|looking for).*?(\w+)', text, re.IGNORECASE)
    return list(set(requirements))

def process_job_listing(job_text):
    cleaned_text = clean_job_listing(job_text)
    requirements = extract_requirements(cleaned_text)
    
    return {
        "cleaned_text": cleaned_text,
        "requirements": requirements
    }

if __name__ == "__main__":
    sample_job = "Software Engineer\nRequires: Python, Java\nLooking for 5+ years of experience"
    processed = process_job_listing(sample_job)
    print(processed)