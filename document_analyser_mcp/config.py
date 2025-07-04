import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Hugging Face API Configuration
    HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
    HUGGING_FACE_MODEL = os.getenv("HUGGING_FACE_MODEL", "cardiffnlp/twitter-roberta-base-sentiment")
    HUGGING_FACE_API_URL = os.getenv("HUGGING_FACE_API_URL", "https://api-inference.huggingface.co/models")
    
    # File paths
    DOCUMENTS_FILE = "data/documents.json"
    
    # API Configuration
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    
    # Text processing limits
    MAX_TEXT_LENGTH = 10000
    DEFAULT_KEYWORD_LIMIT = 5
    
    @classmethod
    def get_sentiment_api_url(cls):
        return f"{cls.HUGGING_FACE_API_URL}/{cls.HUGGING_FACE_MODEL}"
