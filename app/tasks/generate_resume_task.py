import openai
from app.utils.openai_utils import get_openai_client

def generate_optimized_resume(resume_text, job_description):
    client = get_openai_client()
    
    prompt = f"""
    Given the following resume and job description, generate an optimized resume:

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Generate an optimized resume that highlights relevant skills and experience for this job.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are an expert resume optimizer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    sample_resume = "John Doe - Software Engineer\nSkills: Python, Java\nExperience: 3 years"
    sample_job = "Senior Software Engineer\nRequired: Python, AWS, 5+ years experience"
    
    optimized_resume = generate_optimized_resume(sample_resume, sample_job)
    print(optimized_resume)