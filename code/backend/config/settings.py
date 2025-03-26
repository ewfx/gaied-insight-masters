import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    ENV = os.getenv("ENV")  # Default to "local" if ENV is not set
    # API Token
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN")

    GEMENI_API_KEY_TOKEN = os.getenv("GEMENI_API_KEY") or os.environ.get("GEMENI_API_KEY")

    # Model Path
    MODEL_NAME = os.getenv("MODEL_NAME") or os.environ.get("MODEL_NAME") # Default if not set
    OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")
    directory_path = os.getenv("EMAIL_DIRECTORY_PATH") or os.environ.get("EMAIL_DIRECTORY_PATH")  # Make configurable
    ALLOWED_PRIORITY_RULES_FILENAME=os.getenv("ALLOWED_PRIORITY_RULES_FILENAME") or os.environ.get("ALLOWED_PRIORITY_RULES_FILENAME")  # Make configurable
    DATA_DIRECTORY_ATTACHMENTS_PATH=os.getenv("DATA_DIRECTORY_ATTACHMENTS_PATH") or os.environ.get("DATA_DIRECTORY_ATTACHMENTS_PATH")  # Make configurable
    DATA_DIRECTORY_EMAILS_PATH=os.getenv("DATA_DIRECTORY_EMAILS_PATH") or os.environ.get("DATA_DIRECTORY_EMAILS_PATH")  # Make configurable
    # Debugging info
    print(f"Running in {ENV} mode with model path: {MODEL_NAME}")
    print(f"Running in {ENV} mode with TOKEN: {HUGGINGFACE_API_TOKEN}")

settings = Settings()



