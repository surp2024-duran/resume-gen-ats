import re

def clean_resume(text):
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills(text):
    # Implement skill extraction logic
    # This is a simplified example
    skills = re.findall(r'\b(?:Python|Java|C\+\+|JavaScript)\b', text, re.IGNORECASE)
    return list(set(skills))

def process_resume(resume_text):
    cleaned_text = clean_resume(resume_text)
    skills = extract_skills(cleaned_text)
    
    return {
        "cleaned_text": cleaned_text,
        "skills": skills
    }

if __name__ == "__main__":
    sample_resume = "John Doe - Software Engineer\nSkills: Python, Java, C++\nExperience: 5 years"
    processed = process_resume(sample_resume)
    print(processed)