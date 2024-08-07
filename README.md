# Resume Generation and Optimization for ATS Systems

This project leverages OpenAI's gpt-3.5-turbo-0125 model to generate and optimize resumes tailored to job listings, ensuring high compatibility with Applicant Tracking Systems (ATS), with an autonomous pipeline to continue training the model to maximize ATS scoring from EnhanCV.

## Abstract

This project develops an autonomous pipeline for generating and optimizing resumes tailored to specific job listings using OpenAI's GPT-3.5-turbo model. The system is designed to improve resume compatibility with Applicant Tracking Systems (ATS) through continuous learning and fine-tuning. By leveraging cloud services (AWS S3 and MongoDB Atlas) and implementing a feedback loop with manual scoring, the pipeline iteratively enhances its ability to produce high-quality, ATS-friendly resumes. The project incorporates a CI/CD workflow for automated model improvement, making it a robust solution for job seekers looking to optimize their application materials for modern recruitment processes.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Git
- AWS CLI
- MongoDB
- OpenAI API key

## Installation and Local Development For the Backend

1. Clone the repository if you haven't already:
   ```
   git clone https://github.com/surp2024-duran/resume-gen-ats.git
   cd resume-gen-ats
   ```

2. Go to /backend and create and activate a virtual environment:
   ```
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration for .env

```
AWS_ACCESS_KEY_ID=your-aws-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
OPENAI_API_KEY=your-openai-key
OPENAI_ORG=your-openai-org
MONGO_URI=surp24.rwhuwqq.mongodb.net
MONGO_USERNAME=your-mongodb-username
MONGO_PASSWORD=your-mongodb-password
MONGO_DB_NAME=SURP24
MONGO_COLLECTION_NAME=Resumes
MONGO_COLLECTION_EDITED_NAME=Resumes_Post_Edit
S3_BUCKET=resume-gen-ats-raw-data
GITHUB_TOKEN=your-github-token
SLACK_WEBHOOK=your-slack-webhook
PYTZ_TIMEZONE='US/Pacific'
```


## Data Flow

1. **Raw Data Storage**:
   - Raw data (resumes and job postings in CSV format) is stored in the S3 bucket `resume-gen-ats-raw-data`.
   - Raw data is saved to user's local storage at `data/input`

2. **Data Cleaning and Processing**:
   - Data is cleaned and processed using `data_cleanup.py`.
   - Cleaned data is saved to user's local storage at `data/processed` directory as `cleaned_job_postings.csv` and `cleaned_resumes.csv`

3. **Data Generation and Upload**:
   - Cleaned data from the `data/processed` directory is manipulated using `data_generate_resume.py`, which generates and adds the `generated_resume` and `prompt` to the MongoDB `Resumes` collection.
   - With the two new fields, a new CSV file called `resumes_post_edit.csv` is saved to user's local stoarge at `data/output` directory
   - The new documents, which now includes the "generated_resume" and "prompt" fields, is inserted into the `Resumes` collection, replacing the old document that lacked these fields using `data_upload.py`, which is done after all documents are updated with `data_generate_resume.py`
   - So essentially, `Resumes` collection should contain `id, resume_text, job_descriptions, generated_resume, prompt, generated_resume, and prompt`
   - The same documents will also be updated to `july-23-resumes` collection, just as a precaution. 

Note: The fields `score` is out of 100 and `truthfulness` boolean which will be added in the next step by volunteer's manual process of using `data_update.py`

4. **Manual Scoring and Assessment**:
   - Volunteers manually add scores and truthfulness to the `Resumes` collection using `data_update.py` after assessing the resumes through the EnhanCV online interface.
   - Volunteers will manually look at a document in the `Resumes` collection. If they do not already have a `score` and `truthfulness`, then they will use the `data_update.py` to add those two fields. At the end of the `data_update.py`, it should upload the new document with the two new fields onto `july-23-resumes` collection, but also the original `Resumes` collection so it will insert 2 new fields into the same document, not replacing it but adding 2 fields. 

   More fields will be added like `claiming` and `didBy` but they aren't very relevant. 

5. **Model Fine-Tuning**:
   - The model is fine-tuned using the collected feedback via `fine_tuning.py`, with the objective of achieving higher ATS scores.
   - It should take `july-23-resumes` and see to improve that score, as well as to achieve a `truthfulness` value of `true` which is written by the volunteer manually. 

6. **Continuous Integration and Continuous Deployment (CI/CD)**:
   - A CI/CD GitHub Actions workflow continuously trains the model based on the latest feedback, ensuring the model improves over time.
   - This runs every night at 12am PST

7. **Process Repetition**:
   - New data is added to `resume-gen-ats-raw-data`.
   - Data is cleaned with `data_cleanup.py` and saved locally.
   - Cleaned data is uploaded to MongoDB using data_upload.py to the Resumes and the current day's collection `july-23-resumes`and saved locally
   - Resumes are generated with `data_generate_resume.py` and saved locally.
   - Volunteers score and assess the resumes, updating documents  derived from `july-23-resumes` and also updated the document itself in `Resume`
   - The model is fine-tuned with `fine_tuning.py`.
   - At midnight (12 am PST), the CI/CD pipeline pulls documents from the past collection using the naming convention `july-23-resumes`.
   - The fine_tuning.py script generates resumes with better ATS scores from the pulled collection.
   - The updated resumes are uploaded to the next day's collection `july-24-resumes`.
   - Volunteers take the day to label the resumes with score and truthfulness from EnhanCV
   - This process repeats every day at midnight (12 am PST)

## Architecture Diagram

[insert diagram here]


## MongoDB 

### Resumes Collection

- **Fields**:
  - id
  - resume_text
  - job_descriptions
  - generated_resume
  - prompt

### july-23-resumes Collection

- **Fields**:
  - id
  - resume_text
  - job_descriptions
  - generated_resume
  - prompt
  - score
  - truthfulness 

## S3 Buckets 

S3 buckets will really only be used to store large raw datasets. Manipulated data (after we pull it in from S3) should be kept in MongoDB 

- **resume-gen-ats-raw-data**: Stores raw resume and job posting CSV files.
- **resume-gen-ats-processed-data**: Stores cleaned and processed data files.

## Input CSV Files

`resumes.csv` and `postings.csv` are in the `resume-gen-ats-raw-data` S3 bucket

### resumes.csv

- **Fields**:
  - Text
  - Skills
  - Education
  - Experience
  - Additional_Information
  - Software_Developer
  - Front_End_Developer
  - Network_Administrator
  - Web_Developer
  - Project_manager
  - Database_Administrator
  - Security_Analyst
  - Systems_Administrator
  - Python_Developer
  - Java_Developer
  - Labels

### postings.csv

- **Fields**:
  - job_id
  - company_name
  - title
  - description
  - max_salary
  - pay_period
  - location
  - company_id
  - views
  - med_salary
  - min_salary
  - formatted_work_type
  - applies
  - original_listed_time
  - remote_allowed
  - job_posting_url
  - application_url
  - application_type
  - expiry
  - closed_time
  - formatted_experience_level
  - skills_desc
  - listed_time
  - posting_domain
  - sponsored
  - work_type
  - currency
  - compensation_type

