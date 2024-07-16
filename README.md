# Resume Generation and Optimization for ATS Systems

This project leverages OpenAI's gpt-3.5-turbo-0125 model to generate and optimize resumes tailored to job listings, ensuring high compatibility with Applicant Tracking Systems (ATS).

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
│   ├── monitor_fine-tuning.py  # Monitors the fine-tuning process
│   ├── model-testing.py        # Tests the model
│   ├── data-extraction/
│   │   ├── extract_text_from_excel.py  # Extracts text from CSV files
│   │   └── preprocess_text.py  # Preprocesses extracted text
│   └── data-processing/
│       ├── process_resumes.py  # Processes resumes
│       ├── process_job_listings.py  # Processes job listings
│       └── generate_ats_feedback.py  # Generates ATS feedback
├── app/
│   ├── main.py                 # Main application entry point
│   ├── utils/
│   │   ├── openai_utils.py     # Interacts with OpenAI API
│   │   ├── s3_utils.py         # Interacts with S3
│   │   └── mongodb_utils.py    # Interacts with MongoDB
│   └── tasks/
│       ├── process_resume_task.py  # Processes resumes
│       └── generate_resume_task.py # Generates and optimizes resumes
├── data/
│   ├── input/                  # Stores input files
│   ├── processed/              # Stores processed data
│   └── output/                 # Stores output files
├── tests/
│   ├── unit/
│   │   ├── test_data_extraction.py  # Unit tests for data extraction scripts
│   │   ├── test_data_processing.py  # Unit tests for data processing scripts
│   │   └── test_model_utils.py  # Unit tests for model utility functions
│   └── integration/
│       └── test_end_to_end.py   # End-to-end integration tests
├── docs/
│   ├── setup-guide.md          # Guide for setting up the project
│   ├── usage-guide.md          # Guide for using the project
│   └── architecture-diagram.drawio # Architecture diagram of the project
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview and instructions
└── .env                        # Project keys and secrets
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git
- AWS CLI
- MongoDB
- OpenAI API key

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/resume-gen-ats.git
cd resume-gen-ats
```

2. **Create a virtual environment and activate it:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up the environment variables:**

Create a `.env` file in the root directory of your project and add the following variables:

```plaintext
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=surp24.rwhuwqq.mongodb.net
MONGO_USERNAME=your_mongodb_username
MONGO_PASSWORD=your_mongodb_password
MONGO_DB_NAME=SURP24
MONGO_COLLECTION_NAME=Resumes
```

### Usage

1. **Run data extraction and processing scripts:**

```bash
python scripts/data-extraction/extract_text_from_excel.py
python scripts/data-processing/process_resumes.py
python scripts/data-processing/process_job_listings.py
```

2. **Upload processed data to MongoDB:**

```bash
python scripts/data-upload.py
```

3. **Generate and optimize resumes:**

```bash
python app/tasks/generate_resume_task.py
```

4. **Generate ATS feedback:**

```bash
python scripts/data-processing/generate_ats_feedback.py
```

** This might be different from the standard procedure. Initially, we are asking to put this output onto a document and manually feed it to the ATS system. 

5. **Fine-tune the model:**

```bash
python scripts/fine-tuning.py
python scripts/monitor_fine_tuning.py
```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Instructions for Setting Up the `.env` File

1. **Create a `.env` file in the root directory of your project:**

```bash
touch .env
```

2. **Add your environment variables to the `.env` file:**

```plaintext
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=surp24.rwhuwqq.mongodb.net 
MONGO_USERNAME=your_mongodb_username
MONGO_PASSWORD=your_mongodb_password
MONGO_DB_NAME=SURP24
MONGO_COLLECTION_NAME=Resumes
```

Katie or I should have given you these keys. If you don't have them or forget them, let us know. 

3. **Load the environment variables in your scripts:**

In your Python scripts, use the `python-dotenv` package to load the environment variables from the `.env` file:

```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables (for example)
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
# continue with rest of keys or secrets
```

4. **Install the `python-dotenv` package if not already installed:**

Add `python-dotenv` to your `requirements.txt`:

```plaintext
python-dotenv
```

And install it:

```bash
pip install python-dotenv
```

