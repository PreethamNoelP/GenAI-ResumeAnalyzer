import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = 'gemini-pro'

# Batch Processing Configuration
BATCH_SIZE = 10  # Process 10 resumes at a time
MAX_CONCURRENT_REQUESTS = 5  # Maximum concurrent API calls
RATE_LIMIT_DELAY = 1  # Delay between API calls in seconds

# File Processing Configuration
SUPPORTED_FORMATS = ['.pdf', '.docx']
MAX_FILE_SIZE_MB = 10
TEMP_DIR = "temp_files"

# Output Configuration
OUTPUT_DIR = "output"
EXCEL_FILENAME = "resume_analysis_results.xlsx"
JSON_FILENAME = "resume_analysis_results.json"

# UI Configuration
PAGE_TITLE = "AI Resume Analyzer & Chatbot"
LAYOUT = "wide"

# Analysis Configuration
SKILLS_KEYWORDS = [
    "python", "machine learning", "deep learning", "ai", "artificial intelligence",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "opencv",
    "nlp", "computer vision", "data science", "statistics", "sql", "nosql",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github"
]

# Error Messages
ERROR_MESSAGES = {
    "no_api_key": "GEMINI_API_KEY is not set in the .env file",
    "unsupported_format": "Unsupported file format. Please upload PDF or DOCX files.",
    "file_too_large": "File size exceeds maximum limit of 10MB",
    "processing_error": "Error processing file: {}",
    "api_error": "API error occurred: {}"
} 