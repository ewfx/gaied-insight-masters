
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import os
import email
from email import policy
from email.parser import BytesParser
import dateutil.parser
import io
from app.services.classify_prompt import classify_email_with_prompt
from app.services.email_reader import parse_email_bytes, read_emails_from_directory, parse_email
from app.services.duplicate_checker import check_duplicate
from app.models.email_model import EmailData
from app.models.request_type_model import RequestTypeModel
from app.services.retrieve_email_process import process_single_email
from config import settings

router = APIRouter()

# Define the directory where attachments will be saved
SAVE_DIR = Path("data/attachments")
SAVE_FILE_PATH = SAVE_DIR / settings.settings.ALLOWED_PRIORITY_RULES_FILENAME

if not SAVE_DIR.exists():
    SAVE_DIR.mkdir(parents=True)
    print(f"Directory created: {SAVE_DIR}")
else:
    print(f"Directory already exists: {SAVE_DIR}")

@router.post("/process-emails-upload/", response_model=List[EmailData])
async def process_email_files(files: List[UploadFile] = File(...)):
    """Processes multiple email files uploaded from form data."""
    results = []
    for file in files:
        try:
            file_content = await file.read()
            email_result = await process_single_email(file_content, file.filename)
            if email_result:
                email_resp = EmailData(
                    sender=email_result["sender"],
                    subject=email_result["subject"],
                    request_type=email_result["request_type"],
                    sub_request_type=email_result["sub_request_type"],
                    confidence_score=email_result["confidence_score"],
                    duplicate_flag=email_result["duplicate_flag"],
                    all_extracted_numbers=email_result["extracted_numbers_list"]
                )
                results.append(email_resp)
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
    return results


@router.post("/process-email-directory/", response_model=List[EmailData])
async def process_email_directory():
    """Processes email files from a directory specified in an environment variable."""
    directory_path = Path("data/emails")
    #directory_path = settings.settings.directory_path

    if not directory_path:
        raise HTTPException(status_code=400, detail="EMAIL_DIRECTORY_PATH environment variable not set.")

    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        raise HTTPException(status_code=400, detail="Invalid directory path.")

    results = []
    email_files = []
    for file in os.listdir(directory_path):
        if file.endswith(".eml") or file.endswith(".msg") or file.endswith(".txt"):
            email_files.append(os.path.join(directory_path, file))

    for file_path in email_files:
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()
            filename = os.path.basename(file_path)
            email_result = await process_single_email(file_content, filename)
            if email_result:
                email_resp = EmailData(
                    sender=email_result["sender"],
                    subject=email_result["subject"],
                    request_type=email_result["request_type"],
                    sub_request_type=email_result["sub_request_type"],
                    confidence_score=email_result["confidence_score"],
                    duplicate_flag=email_result["duplicate_flag"],
                    all_extracted_numbers=email_result["extracted_numbers_list"]
                )
                results.append(email_resp)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    return results


@router.post("/upload-priority-rules/",
             description="""
Upload a JSON file containing the priority rules for request type identification and numerical extraction.
**Sample JSON file structure:**

```json
{
  "priority_rules": {
    "is_prioritization_extraction": true,
    "request_type_identification": {
      "order": ["email_content", "document_content"],
      "fallback": "document_content"
    },
    "numerical_field_extraction": {
      "preferred_source": ["attachments"],
      "fallback": "email_body"
    },
    "banking_numeric_keys": [
      "loan_amount",
      "balance",
      "interest_rate"
      .......
    ]
  }
}"
"""
)
async def upload_rules(file: UploadFile = File(...)):

    # Validate filename
    if file.filename != settings.settings.ALLOWED_PRIORITY_RULES_FILENAME:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file name. Please use the appropriate file name: {settings.settings.ALLOWED_PRIORITY_RULES_FILENAME}"
        )
    
   # Check if file is a JSON
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Only JSON files are allowed.")

    # Save file to the specified location
    try:
        file_content = await file.read()
        with open(SAVE_FILE_PATH, "wb") as f:
            f.write(file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
    
    return {"message": "Rules JSON uploaded successfully."}
