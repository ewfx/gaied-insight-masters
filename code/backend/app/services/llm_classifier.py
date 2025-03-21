# from llama_cpp import Llama
# import os

# MODEL_PATH = os.getenv("MODEL_PATH", "path/to/llama/model.bin")

# llm = Llama(model_path=MODEL_PATH)

# def classify_email(content: str):
#     """Uses LLaMA to classify an email's type, priority, and confidence score."""
#     prompt = f"Classify this email:\n{content}\nRequest Type, Priority, Confidence Score:"
#     response = llm(prompt)

#     # Extract response text
#     result = response["choices"][0]["text"].strip().split(",")

#     request_type = result[0].strip() if len(result) > 0 else "Unknown"
#     priority = result[1].strip() if len(result) > 1 else "Low"
#     confidence = float(result[2].strip()) if len(result) > 2 else 0.5

#     return request_type, priority, confidence



import requests
import os

from config import settings

#HF_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")  # Set your API key in .env
#MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"  # You can change this to another LLaMA model

def classify_email(email_body):
    """Classifies email using Hugging Face LLaMA API."""
    
    api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
    headers = {"Authorization": f"Bearer {settings.settings.HUGGINGFACE_API_TOKEN}"}
    
    response = requests.post(api_url, headers=headers, json={"inputs": email_body})

    if response.status_code == 200:
        output = response.json()
        return output  # Modify based on response structure
    
    raise Exception(f"Hugging Face API error: {response.text}")
