import requests
import json

def send_resume_to_ats(resume_text):
    # This is a mock ATS API endpoint
    ats_api_url = "https://mock-ats-api.example.com/analyze"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_ATS_API_KEY"
    }
    
    payload = {
        "resume": resume_text
    }
    
    response = requests.post(ats_api_url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"ATS API request failed with status code {response.status_code}")

def generate_ats_feedback(resume_text):
    ats_response = send_resume_to_ats(resume_text)
    
    score = ats_response.get("score", 0)
    feedback = ats_response.get("feedback", "No feedback available")
    
    return {
        "score": score,
        "feedback": feedback
    }

if __name__ == "__main__":
    sample_resume = "John Doe - Software Engineer\nSkills: Python, Java\nExperience: 3 years"
    feedback = generate_ats_feedback(sample_resume)
    print(feedback)