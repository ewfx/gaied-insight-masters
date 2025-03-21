import os
import email
from email import policy
from email.parser import BytesParser
from typing import List

def read_emails_from_directory(directory: str) -> List[str]:
    """Reads email files from a given directory"""
    emails = []
    for file in os.listdir(directory):
        if file.endswith(".eml") or file.endswith(".msg") or file.endswith(".txt"):
            emails.append(os.path.join(directory, file))
    return emails

def parse_email(file_path: str) -> dict:
    """Parses email file and extracts metadata, body, and attachments."""
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    body = ""
    attachments = []
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
        elif part.get_filename():
            attachments.append(part.get_filename())

    return {
        "sender": msg["From"],
        "subject": msg["Subject"],
        "date": msg["Date"],
        "body": body,
        "attachments": attachments
    }
