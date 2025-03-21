import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN")
    MODEL_PATH = os.getenv("MODEL_PATH", "./models/llama-7b")  # Default if not set
    OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")
    EMAIL_DIRECTORY = "data/emails"
    #MODEL_NAME = "meta-llama/Llama-2-7b"    

    # if not MODEL_PATH or not os.path.exists(MODEL_PATH):
    #     raise ValueError(f"Model path does not exist: {MODEL_PATH}")

settings = Settings()



