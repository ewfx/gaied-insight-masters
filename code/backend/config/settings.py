import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    ENV = os.getenv("ENV", "local")  # Default to "local" if ENV is not set
    # API Token
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN") or os.environ.get("HUGGINGFACE_API_TOKEN")

    # Model Path
    MODEL_NAME = os.getenv("MODEL_NAME") or os.environ.get("MODEL_NAME") # Default if not set
    OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")
    directory_path = os.getenv("EMAIL_DIRECTORY_PATH") or os.environ.get("EMAIL_DIRECTORY_PATH")  # Make configurable
    #MODEL_NAME = "meta-llama/Llama-2-7b"    

     # Ensure model path exists
    # if not os.path.exists(MODEL_PATH):
    #     os.makedirs(MODEL_PATH, exist_ok=True)

    # # Validate required variables
    # if not HUGGINGFACE_API_TOKEN:
    #     raise ValueError("Missing HUGGINGFACE_API_TOKEN. Please set it in the environment variables or .env file.")

    # Debugging info
    print(f"Running in {ENV} mode with model path: {MODEL_NAME}")
    print(f"Running in {ENV} mode with TOKEN: {HUGGINGFACE_API_TOKEN}")

settings = Settings()



