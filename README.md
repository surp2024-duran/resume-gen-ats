# Resume Generation and Optimization for ATS Systems

This project leverages OpenAI's gpt-3.5-turbo-0125 model to generate and optimize resumes tailored to job listings, ensuring high compatibility with Applicant Tracking Systems (ATS).

## Abstract

In this project, data flows from raw input files (resumes and job postings in CSV format) stored in the S3 bucket resume-gen-ats-raw-data. The data is cleaned and processed using Python scripts such as data_cleanup.py, which filters and preprocesses the text. The cleaned data is then saved back to the S3 bucket resume-gen-ats-processed-data. Subsequently, the script data_upload.py uploads this processed data to two MongoDB collections: Resumes (fields: id, resume_text, job_descriptions, generated_resume, prompt) and Resume_Post_Edit (fields: id, resume_text, job_descriptions, generated_resume, prompt, score, truthfulness). Using OpenAI's GPT-3.5-turbo-0125 model, the script generate_resume_task.py generates and optimizes resumes based on job descriptions. Currently, volunteers use the data_update.py script to manually add fields like "truthfulness" and update scores through a MongoDB interface as we do not have access to a convenient ATS API. The collected feedback and labels are used to fine-tune the model via the fine-tuning.py script for continuous improvement. The entire workflow is automated using a CI/CD pipeline defined in the GitHub Actions workflow ci.yml, ensuring seamless data processing, model training, and deployment.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Data Flow](#data-flow)
8. [Contributing](#contributing)
9. [License](#license)

## Project Overview

This project automates the process of resume optimization for job applications. It uses machine learning to generate resumes tailored to specific job descriptions, with the goal of improving compatibility with Applicant Tracking Systems (ATS).

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Git
- AWS CLI
- MongoDB
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/resume-gen-ats.git
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

## Configuration

1. Create a `.env` file in the root directory of the project.

2. Add the following environment variables to the `.env` file:
   ```
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   OPENAI_API_KEY=your_openai_api_key
   MONGO_URI=surp24.rwhuwqq.mongodb.net
   MONGO_USERNAME=your_mongodb_username
   MONGO_PASSWORD=your_mongodb_password
   MONGO_DB_NAME=SURP24
   MONGO_COLLECTION_NAME=Resumes
   MONGO_COLLECTION_EDITED_NAME=Resumes_Post_Edit
   GITHUB_TOKEN=your_github_token
   SLACK_WEBHOOK=your_slack_webhook_url
   ```

   Replace the placeholder values with your actual credentials and configurations.

## Usage

1. Data Preparation:
   - Place your raw resume and job posting CSV files in the S3 bucket `resume-gen-ats-raw-data`.

2. Data Cleanup:
   - Run the data cleanup script:
     ```
     python scripts/data_cleanup.py
     ```
   - This will process the raw data and save the cleaned data to the S3 bucket `resume-gen-ats-processed-data`.

3. Data Upload:
   - Upload the processed data to MongoDB:
     ```
     python scripts/data_upload.py
     ```

4. Generate Optimized Resumes:
   - Run the resume generation script:
     ```
     python app/tasks/generate_resume_task.py
     ```

5. Manual Review:
   - Volunteers can use the `data_update.py` script to manually add scores and truthfulness ratings:
     ```
     python scripts/data_update.py
     ```

6. Model Fine-tuning:
   - Fine-tune the model using the collected feedback:
     ```
     python scripts/fine-tuning.py
     ```

7. Monitoring and Testing:
   - Monitor the fine-tuning process:
     ```
     python scripts/monitor_fine-tuning.py
     ```
   - Run model tests:
     ```
     python scripts/model-testing.py
     ```

8. CI/CD Pipeline:
   - The project includes a GitHub Actions workflow defined in `.github/workflows/ci.yml` that automates the entire process.

## Project Structure

[Include the project structure here as provided in the original document]

## Data Flow

1. Raw data (resumes and job postings in CSV format) is stored in the S3 bucket `resume-gen-ats-raw-data`.
2. Data is cleaned and processed using `data_cleanup.py`.
3. Cleaned data is saved to the S3 bucket `resume-gen-ats-processed-data`.
4. Processed data is uploaded to MongoDB collections (`Resumes` and `Resume_Post_Edit`) using `data_upload.py`.
5. Resumes are generated and optimized using `generate_resume_task.py`.
6. Volunteers manually add scores and truthfulness ratings using `data_update.py`.
7. The model is fine-tuned using the collected feedback via `fine-tuning.py`.

## Contributing

Contributions to this project are welcome. Please ensure you follow the coding standards and submit pull requests for any new features or bug fixes.

