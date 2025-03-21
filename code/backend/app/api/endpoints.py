from fastapi import APIRouter
from app.services.email_reader import read_emails_from_directory, parse_email
from app.services.llm_classifier import classify_email
from app.services.duplicate_checker import check_duplicate
from app.models.email_model import EmailData

router = APIRouter()

@router.get("/process-emails/")
def process_emails(directory: str):
    """Processes emails from a given directory."""
    email_files = read_emails_from_directory(directory)
    results = []

    for file in email_files:
        email_data = parse_email(file)
        request_type, priority, confidence = classify_email(email_data["body"])
        duplicate_flag, duplicate_reason = check_duplicate(email_data["body"])

        email_obj = EmailData(
            sender=email_data["sender"],
            subject=email_data["subject"],
            date=email_data["date"],
            body=email_data["body"],
            attachments=email_data["attachments"],
            request_type=request_type,
            priority=priority,
            confidence_score=confidence,
            duplicate_flag=duplicate_flag,
            duplicate_reason=duplicate_reason
        )

        results.append(email_obj)

    return results
