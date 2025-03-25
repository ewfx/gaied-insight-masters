
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
from app.services.gemeni_classification import analyze_intent, classify_email_gemeni, extract_text_from_attachment, get_primary_intent
from app.services.retrieve_email_process import process_single_email
from config import settings

router = APIRouter()


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
                )
                results.append(email_resp)
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
    return results


@router.post("/process-email-directory/", response_model=List[EmailData])
async def process_email_directory():
    """Processes email files from a directory specified in an environment variable."""
    directory_path = settings.settings.directory_path

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
                )
                results.append(email_resp)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    return results
