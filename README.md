# Resume Generation and Optimization for ATS Systems

This project leverages OpenAI's GPT-3.5-turbo-0125 model to generate and optimize resumes tailored to job listings, ensuring high compatibility with Applicant Tracking Systems (ATS). It includes an autonomous pipeline to continue training the model to maximize ATS scoring from EnhanCV.

The purpose was to test prompt engineering theories through OpenAI's model.

This project runs its frontend on Netlify and backend on Heroku.

## Website

See statistics at [https://surp2024-duran.netlify.app/](https://surp2024-duran.netlify.app/)

## Technologies

**Frontend:**
- React
- Chart.js
- Franken-UI (UI-Kit)

**Backend:**
- Python
- OpenAI

**Database & Deployment:**
- MongoDB
- AWS S3
- Netlify
- Heroku

## Installation and Local Development for the Backend

1. Clone the repository if you haven't already:
   ```bash
   git clone https://github.com/surp2024-duran/resume-gen-ats.git
   cd resume-gen-ats
   ```

2. Go to `/backend` and create and activate a virtual environment:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Installation and Local Development for the Frontend

1. Clone the repository if you haven't already:
   ```bash
   git clone https://github.com/surp2024-duran/resume-gen-ats.git
   cd resume-gen-ats
   ```

2. Go to `/frontend` and install dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Start the frontend:
   ```bash
   npm start
   ```

## Configuration for `.env`

```bash
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_REGION=us-east-1
OPENAI_API_KEY=your-openai-api-key
OPENAI_ORG=your-openai-org-id
MONGO_URI=your-mongo-uri
MONGO_FULL_URI=your-mongo-full-uri
MONGO_USERNAME=your-mongo-username
MONGO_PASSWORD=your-mongo-password
MONGO_DB_NAME=your-db-name
MONGO_COLLECTION_NAME=your-collection-name
MONGO_COLLECTION_EDITED_NAME=your-edited-collection-name
S3_BUCKET=your-s3-bucket-name
GITHUB_TOKEN=your-github-token
SLACK_WEBHOOK_URL=your-slack-webhook-url
PYTZ_TIMEZONE='US/Pacific'
S3_BUCKET_TEST=your-test-s3-bucket-name
ESLINT_NO_DEV_ERRORS=true
REACT_APP_API_URL=your-react-app-api-url
```

## Project Process

This project was conducted with two tech leads and a team of volunteers.

The process began with tech leads creating initial scripts and pipelines, which created a loop of continually generated MongoDB collections. These collections were named using the convention `month-date-resumes`, created every midnight (12am PST).

Volunteers were required to manually label each collection by pasting the generated resume content (from an OpenAI response) into a text editor, like Google Docs or Overleaf (for LaTeX resumes), and inputting them into the website EnhanCV to receive a score out of 100. Volunteers also added a `truthfulness` boolean to the document at their discretion.

This labeling process occurred daily, and we compared statistics to see which prompt scored the best.

## MongoDB

MongoDB stores collections named from `july-23-resumes` to `august-14-resumes` (as of the time of writing). Most collections have exactly 219 documents, which was chosen as a comparison point, even though the original collection had about 1000 documents. The team settled on 219 as a manageable number.

## S3 Buckets

S3 buckets are used primarily to store large raw datasets. Manipulated data, after pulling it from S3, is stored in MongoDB.

- **resume-gen-ats-raw-data**: Stores raw resume and job posting CSV files.
- **resume-gen-ats-processed-data**: Stores cleaned and processed data files.

## Input CSV Files

`resumes.csv` and `postings.csv` are stored in the `resume-gen-ats-raw-data` S3 bucket.

### resumes.csv

**Fields:**
- Text
- Skills
- Education
- Experience
- Additional_Information
- Software_Developer
- Front_End_Developer
- Network_Administrator
- Web_Developer
- Project_Manager
- Database_Administrator
- Security_Analyst
- Systems_Administrator
- Python_Developer
- Java_Developer
- Labels

### postings.csv

**Fields:**
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