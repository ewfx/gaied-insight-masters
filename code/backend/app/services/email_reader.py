import os
import email
from email import policy
from email.parser import BytesParser
import re
from typing import Dict, List, Optional
import dateutil
from fastapi import HTTPException

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

def parse_email_bytes(file_content: bytes, filename: str) -> Optional[Dict]:
    """Parses email bytes, extracts attachments, and handles email chains."""
    try:
        msg = email.message_from_bytes(file_content)
        sender = msg["from"]
        subject = msg["subject"]
        body = ""
        attachments = []
        email_chain_text = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body += part.get_payload(decode=True).decode()
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    html = part.get_payload(decode=True).decode()
                    body += ''.join(c if ord(c) < 128 else ' ' for c in html.replace("<br>", "\n").replace("<p>", "\n").replace("</p>","\n").replace("<div>","\n").replace("</div>","\n").replace("<span>"," ").replace("</span>", " "))

                elif "attachment" in content_disposition:
                    attachment_data = part.get_payload(decode=True)
                    attachments.append({
                        "filename": part.get_filename(),
                        "content": attachment_data,
                    })
            email_chain_text = process_email_chain(msg) #only process if it is multipart.
        else:
            body = msg.get_payload(decode=True).decode()

        # Handle email chains (add logic based on your needs)
        # email_chain_text = process_email_chain(msg) #see full code in previous response.

        return {
            "sender": sender if sender else "Unknown Sender", #added default value.
            "subject": subject if subject else "No Subject", #added default value.
            "body": body,
            "attachments": attachments,
            "email_chain_text": email_chain_text
        }

    except Exception as e:
        print(f"Error parsing email: {e}")
        return None
    

def process_email_chain(email_message):
    """
    Detects and processes email chains, extracting text from each email.
    """
    try:
        if isinstance(email_message, str):
            msg = email.message_from_string(email_message)
        else:
            msg = email_message

        chain = []
        full_text = ""

        # Check for nested email headers (From:, Date:) or quoted text
        if has_nested_emails(msg):
            # Parse the email and extract the chain
            chain = extract_email_chain(msg)

            for email_part in chain:
                full_text += extract_text_from_email(email_part) + "\n"
        else:
            # No nested emails, just extract the text from the current email
            full_text = extract_text_from_email(msg)

        return full_text

    except Exception as e:
        print(f"Error processing email chain: {e}")
        return extract_text_from_email(email_message) #default to just the email.

def has_nested_emails(msg):
    """
    Detects if an email contains nested emails based on headers or quoted text.
    """
    body = get_email_body_text(msg)

    # Check for multiple 'From:' and 'Date:' headers in the body
    if body:
        if len(re.findall(r"^From:.*", body, re.MULTILINE)) > 1 or \
           len(re.findall(r"^Date:.*", body, re.MULTILINE)) > 1 or \
           len(re.findall(r"^>.*", body, re.MULTILINE)) > 5: #arbitrary number of quoted lines.
            return True
    return False

def extract_email_chain(msg):
    """
    Extracts the individual emails from a nested email chain.
    """
    chain = []
    #this is a very basic attempt at parsing the email chain. It is not perfect, and will need to be improved based on specific email formatting.
    body = get_email_body_text(msg)
    if not body:
        return [msg] #if no body, then return the message.

    #basic email chain splitting.
    emails = re.split(r"(^From:.*?\n^Date:.*?(\n\n|\r\n\r\n))", body, flags=re.MULTILINE | re.DOTALL)
    if len(emails) > 1:
        for i in range(1, len(emails), 2):
            email_part = emails[i] + emails[i+1]
            try:
                chain.append(email.message_from_string(email_part))
            except Exception as e:
                print(f"Error parsing email part: {e}")
                pass #if error, skip the email part.

    if not chain:
        chain = [msg] #if no chain, then return the original email.

    return chain

def extract_text_from_email(email_message):
    try:
        text = ""
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                text += part.get_payload(decode=True).decode()
            elif part.get_content_type() == "text/html":
                html = part.get_payload(decode=True).decode()
                text += ''.join(c if ord(c) < 128 else ' ' for c in html.replace("<br>", "\n").replace("<p>", "\n").replace("</p>","\n").replace("<div>","\n").replace("</div>","\n").replace("<span>"," ").replace("</span>", " "))

        return text
    except Exception as e:
        print(f"Error parsing email: {e}")
        return ""
    
def get_email_body_text(msg):
    """
    Gets the email body text.
    """
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode()
            elif part.get_content_type() == "text/html":
                body += part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()
    return body