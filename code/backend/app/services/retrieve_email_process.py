
from typing import Optional
from app.services.duplicate_checker import check_duplicate
from app.services.email_reader import parse_email_bytes
from app.services.gemeni_classification import classify_email_gemeni, extract_text_from_attachment


async def process_single_email(file_content: bytes, filename: str) -> Optional[dict]:
    """Processes a single email content."""
    email_data = parse_email_bytes(file_content, filename)
    if email_data:
        attachment_text = ""
        for attachment in email_data["attachments"]:
            attachment_text += extract_text_from_attachment(attachment["content"], attachment["filename"])

        email_chain_text = email_data["email_chain_text"]
        email_body_text = email_data["body"]

        # 1. Separate Classification:
        document_result = classify_email_gemeni(email_data["subject"], attachment_text) if attachment_text else ("Unknown", "Unknown", "0")
        email_chain_result = classify_email_gemeni(email_data["subject"], email_chain_text) if email_chain_text else ("Unknown", "Unknown", "0")
        primary_email_result = classify_email_gemeni(email_data["subject"], email_body_text)

        # 2. Confidence Score Comparison:
        document_confidence = float(document_result[2])
        email_chain_confidence = float(email_chain_result[2])
        primary_email_confidence = float(primary_email_result[2])

        best_result = primary_email_result  # Default to email body
        if document_confidence > primary_email_confidence and document_confidence > email_chain_confidence:
            best_result = document_result
        elif email_chain_confidence > primary_email_confidence and email_chain_confidence > document_confidence:
            best_result = email_chain_result

        # 3. Refined Classification:
        request_type = best_result[0]
        sub_request_type = best_result[1]
        confidence_score = best_result[2]

        duplicate_flag, duplicate_reason = check_duplicate(email_data["body"])
        email_obj = {
            "sender": email_data["sender"],
            "subject": email_data["subject"],
            "request_type": request_type,
            "sub_request_type": sub_request_type,
            "confidence_score": confidence_score,
            "duplicate_flag": duplicate_flag,
        }
        return email_obj
    else:
        print(f"Parsing failed for file: {filename}")
        return None