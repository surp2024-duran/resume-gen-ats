import openai
from app.utils.openai_utils import get_openai_client
from app.utils.mongodb_utils import get_mongodb_client

def prepare_training_data(mongodb_client):
    db = mongodb_client["SURP24"]
    collection = db["Resume_Post_Edit"]
    
    training_data = []
    for doc in collection.find({"score": {"$exists": True}, "truthfulness": {"$exists": True}}):
        training_data.append({
            "messages": [
                {"role": "system", "content": "You are an expert resume optimizer."},
                {"role": "user", "content": f"Resume: {doc['resume_text']}\nJob Description: {doc['job_descriptions']}"},
                {"role": "assistant", "content": doc['generated_resume']}
            ]
        })
    
    return training_data

def fine_tune_model(training_data):
    client = get_openai_client()
    
    file = client.files.create(
        file=open("training_data.jsonl", "rb"),
        purpose='fine-tune'
    )
    
    fine_tuning_job = client.fine_tuning.jobs.create(
        training_file=file.id,
        model="gpt-3.5-turbo-0125"
    )
    
    return fine_tuning_job.id

if __name__ == "__main__":
    mongodb_client = get_mongodb_client()
    training_data = prepare_training_data(mongodb_client)
    
    # Save training data to a JSONL file
    with open("training_data.jsonl", "w") as f:
        for item in training_data:
            f.write(json.dumps(item) + "\n")
    
    job_id = fine_tune_model(training_data)
    print(f"Fine-tuning job started with ID: {job_id}")