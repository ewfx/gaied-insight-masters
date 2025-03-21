from .email_reader import read_email
from ..models.email_model import EmailData

def parse_email(file_path: str) -> EmailData:
    email_data = read_email(file_path)
    return EmailData(
        sender=email_data["sender"],
        recipient=email_data["recipient"],
        subject=email_data["subject"],
        body=email_data["body"],
        attachments=email_data["attachments"]
    )
