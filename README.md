# Resume Generation and Optimization for ATS Systems

This project leverages OpenAI's gpt-3.5-turbo-0125 model to generate and optimize resumes tailored to job listings, ensuring high compatibility with Applicant Tracking Systems (ATS), with an autonomous pipeline to continue training the model to maximize ATS scoring from EnhanCV.

## Table of Contents

1. [Abstract](#abstract)
2. [Prerequisites](#prerequisites)
3. [Installation and Local Development](#installation)
4. [For Volunteers](#for-volunteers)
5. [How to Run Manually and Automatically](#how-to-run-manually-and-automatically)
   - [Manual Execution](#manual-execution)
   - [Automatic Execution](#automatic-execution)
6. [Configuration for .env](#configuration-for-env)
7. [Project Structure](#project-structure)
8. [Thoughts Aloud](#thoughts-aloud)
9. [Data Flow](#data-flow)
10. [MongoDB Collections](#mongodb-collections)
    - [Resumes Collection](#resumes-collection)
    - [Resumes_Post_Edit Collection](#resumes_post_edit-collection)
11. [S3 Buckets](#s3-buckets)
12. [Input CSV Files](#input-csv-files)
13. [Contributing](#contributing)

## Abstract

This project develops an autonomous pipeline for generating and optimizing resumes tailored to specific job listings using OpenAI's GPT-3.5-turbo model. The system is designed to improve resume compatibility with Applicant Tracking Systems (ATS) through continuous learning and fine-tuning. By leveraging cloud services (AWS S3 and MongoDB Atlas) and implementing a feedback loop with manual scoring, the pipeline iteratively enhances its ability to produce high-quality, ATS-friendly resumes. The project incorporates a CI/CD workflow for automated model improvement, making it a robust solution for job seekers looking to optimize their application materials for modern recruitment processes.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Git
- AWS CLI
- MongoDB
- OpenAI API key

## Installation and Local Development (do this everytime you develop)

1. Clone the repository if you haven't already:
   ```
   git clone https://github.com/surp2024-duran/resume-gen-ats.git
   cd resume-gen-ats
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## For Volunteers
1. **Setup your .env file** (see the Configuration for .env section below).

You need to create a `.env` file at the root of this project. In order words, the `.env` file you creat should be at the same directory "level" as the `README.md` or `requirements.txt`

2. Run the script:
   ```bash
   python scripts/data_update.py
   ```
3. Open and log in to [cloud.mongodb.com](https://cloud.mongodb.com).
4. Follow the instructions provided by the script.

**Note:** We have a special field called "claiming" that is added to the document while you are editing. This prevents multiple people from working on the same document simultaneously. If the "claiming" field is set to true when you run the script for a selected document, it will skip that document and move on to the next one.

## How to Run Manually and Automatically

### Manual Execution

To run the pipeline manually, follow these steps:

1. Ensure your `.env` file is properly configured with all necessary credentials.

2. Run the data cleanup script:
   ```
   python scripts/data_cleanup.py
   ```
   This will read raw data from S3, clean it, and save it to `data/processed`.

3. Generate optimized resumes:
   ```
   python scripts/data_generate_resume.py
   ```
   This script reads from `data/processed` and outputs to `data/output`.

4. Upload the generated resumes to MongoDB:
   ```
   python scripts/data_upload.py
   ```
   This uploads the data from `data/output` to the `Resumes` collection in MongoDB.

5. For manual scoring and assessment (to be done by volunteers):
   ```
   python scripts/data_update.py
   ```
   This allows volunteers to add scores and truthfulness ratings, updating the `Resumes_Post_Edit` collection.

6. To fine-tune the model based on the feedback:
   ```
   python scripts/fine_tuning.py
   ```

### Automatic Execution

The project is set up with a GitHub Actions workflow for automatic execution. The workflow is defined in `.github/workflows/ci.yml` and runs daily at midnight PST. Here's how it works:

1. The workflow is triggered automatically at the scheduled time.

2. It runs through all the scripts in sequence: `data_cleanup.py`, `data_generate_resume.py`, `data_upload.py`, and `fine_tuning.py`.

3. The `data_update.py` script is not included in the automatic workflow as it requires manual input from volunteers.

To set up automatic execution:

1. Ensure your repository is connected to GitHub Actions.

2. Add all necessary secrets (AWS credentials, MongoDB credentials, OpenAI API key, etc.) to your GitHub repository's secrets.

3. The workflow will run automatically based on the schedule defined in the `ci.yml` file.

To manually trigger the automatic workflow:

1. Go to your GitHub repository.
2. Click on the "Actions" tab.
3. Select the workflow "Resume Generation and Optimization Pipeline" (or whatever name you've given it in `ci.yml`).
4. Click "Run workflow" and select the branch you want to run it on.

This setup allows for both manual execution for testing and development purposes, and automatic execution for continuous improvement of the model and generated resumes.

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
SLACK_WEBHOOK=https://hooks.slack.com/services/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
```

## Project Structure

```
resume-gen-ats/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline definition
├── scripts/
│   ├── data_upload.py          # Uploads cleaned or processed data to MongoDB
│   ├── data_cleanup.py         # Cleans up input data
│   ├── data_update.py          # Adds score and truthfulness to output 
│   ├── fine-tuning.py          # Fine-tunes the GPT model
│   ├── data_generate_resume.py # Generates resume to job description in 1:1 relationship
│   
├── app/
│   ├── main.py                 # Main application entry point
│   
├── data/
│   ├── input/                  # Stores input files
│   ├── processed/              # Stores processed data
│   └── output/                 # Stores output files
├── util/
│   ├── reduce_csv_for_test.py  # file for testing
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview and instructions
└── .env                        # Project keys and secrets
```

## Thoughts Aloud

Data_cleanup.py should still read from S3, but save those raw files into input. you are right though that it should save cleane data to data/processed
then data_generate_resume.py should be ran, reading from data/procesed and outputting to data/output then data_upload.py reads from data/output to send to the Resumes collection. then data_update.py is done on the volunteer's on time, which will happen randomly throughout each week to manually update score and truthfulness. every document will be manually done, and uploaded to the Resumes_Post_Edit collection 

## Other Testing Features

S3_BUCKET_TEST=ci-cd-workflow-test-bucket contains `reduced_postings.csv` and `reduced_resumes.csv` which both have 10 rows. This is to test the fine-tuning functions

## Data Flow

1. **Raw Data Storage**:
   - Raw data (resumes and job postings in CSV format) is stored in the S3 bucket `resume-gen-ats-raw-data`.
   - Raw data is saved to user's local storage at `data/input`

2. **Data Cleaning and Processing**:
   - Data is cleaned and processed using `data_cleanup.py`.
   - Cleaned data is saved to user's local storage at `data/processed` directory

3. **Data Generation and Upload**:
   - Cleaned data from the S3 bucket `resume-gen-ats-processed-data` is manipulated using `data_generate_resume.py`, which generates and adds the "generated_resume" and "prompt" to the `Resumes` collection.
   - With the two new fields, a new CSV file called `resumes_post_edit.csv` is saved to user's local stoarge at `data/output` directory
   - The new document, which now includes the "generated_resume" and "prompt" fields, is inserted into the `Resumes_Post_Edit` collection, replacing the old document that lacked these fields using `data_upload.py`.
   - So essentially, `Resumes` collection should contain `id, resume_text, job_descriptions, generated_resume, prompt` and then `Resumes_Post_Edit` collection should contain the former 5 fields and the additional `

score` out of 100 and `truthfulness` boolean which will be added in the next step by volunteer's manual process of using `data_update.py`

4. **Manual Scoring and Assessment**:
   - Volunteers manually add scores and truthfulness to the `Resumes` collection using `data_update.py` after assessing the resumes through the EnhanCV online interface.
   - Volunteers will manually look at a document in the `Resumes` collection. If they do not already have a `score` and `truthfulness`, then they will use the `data_update.py` to add those two fields. At the end of the `data_update.py`, it should upload the new document with the two new fields onto `Resumes_Post_Edit` collection. 

5. **Model Fine-Tuning**:
   - The model is fine-tuned using the collected feedback via `fine_tuning.py`, with the objective of achieving higher ATS scores.
   - It should take `Resumes_Post_Edit` and see to improve that score, as well as to achieve a `truthfulness` value of `true` which is written by the volunteer manually. 

6. **Continuous Integration and Continuous Deployment (CI/CD)**:
   - A CI/CD GitHub Actions workflow continuously trains the model based on the latest feedback, ensuring the model improves over time.

7. **Process Repetition**:
   - New data is added to `resume-gen-ats-raw-data`.
   - Data is cleaned with `data_cleanup.py` and saved locally.
   - Resumes are generated with `data_generate_resume.py` and saved locally.
   - Cleaned data is uploaded to MongoDB with `data_upload.py` to the `Resumes` collection and saved locally.
   - Volunteers score and assess the resumes, updating documents `Resumes_Post_Edit` derived from `Resumes`
   - The model is fine-tuned with `fine_tuning.py`.
   - The CI/CD workflow ensures continuous improvement at midnight every day at 12am PST.

## MongoDB Collections

### Resumes Collection

- **Fields**:
  - id
  - resume_text
  - job_descriptions
  - generated_resume
  - prompt

### Resumes_Post_Edit Collection

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

## Contributing

Contributions to this project are welcome. Please ensure you follow the coding standards and submit pull requests for any new features or bug fixes.