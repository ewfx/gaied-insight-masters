
import json
import os
from pathlib import Path
import re
from typing import List, Optional
from app.services.duplicate_checker import check_duplicate
from app.services.email_reader import parse_email_bytes
from app.services.gemeni_classification import classify_email_gemeni, extract_key_number_with_llm, extract_text_from_attachment
from config import settings


async def process_single_email(file_content: bytes, filename: str) -> Optional[dict]:
    """Processes a single email content."""
    # Load customizable priority rules
    rules = load_priority_rules()  # Expected to return a dict with "priority_rules" key
    priority_config = rules.get("priority_rules", {})
    use_priority = priority_config.get("is_prioritization_extraction", False)
    all_extracted_numbers = []  # This will hold the combined results from all attachments

    # Parse the email into its components
    email_data = parse_email_bytes(file_content, filename)
    if email_data:
        # attachment_text = ""
        # for attachment in email_data["attachments"]:
        #     attachment_text += extract_text_from_attachment(attachment["content"], attachment["filename"])

        email_chain_text = email_data["email_chain_text"]
        email_body_text = email_data["body"]

        # Process attachments: extract text and numerical fields
        attachment_text = ""
        extracted_numbers = []
        for attachment in email_data.get("attachments", []):
            text = extract_text_from_attachment(attachment["content"], attachment["filename"])
            attachment_text += text + "\n"
            # extracted_numbers.extend(extract_key_number_with_llm(text,rules))
            extracted_numbers_json = extract_key_number_with_llm(text, rules)
            if extracted_numbers_json:
                try:
                    parsed_result = json.loads(extracted_numbers_json)  # Convert JSON string to Python object
                    # Check if the parsed result is a list; if so, merge it into our overall list.
                    if isinstance(parsed_result, list):
                        all_extracted_numbers.extend(parsed_result)
                    else:
                        all_extracted_numbers.append(parsed_result)
                except Exception as e:
                    print("Error parsing JSON result from LLM:", e)

        # Choose classification logic based on priority configuration
        if use_priority:
            # -- Priority Based Extraction Logic --
            identification_order = priority_config.get("request_type_identification", {}).get("order", [])
            classification_source = ""
            if "email_content" in identification_order and email_body_text.strip():
                classification_source = email_body_text
            elif "document_content" in identification_order and attachment_text.strip():
                classification_source = attachment_text
            else:
                classification_source = email_body_text  # default fallback
            
            primary_result = classify_email_gemeni(email_data["subject"], classification_source, rules)

            # special condition to check if priority is email content and email has multi thread then we 
            # have to compare confidence score with primary confidence score 
            if "email_content" in identification_order:
                email_chain_result = classify_email_gemeni(email_data["subject"], email_chain_text, rules) if email_chain_text else ("Unknown", "Unknown", "0")
                email_chain_confidence = float(email_chain_result[2])
                primary_email_confidence = float(primary_result[2])
                if email_chain_confidence > primary_email_confidence and email_chain_confidence:
                    primary_result  = email_chain_result

        else:
            # 1. Separate Classification:
            document_result = classify_email_gemeni(email_data["subject"], attachment_text, rules) if attachment_text else ("Unknown", "Unknown", "0")
            email_chain_result = classify_email_gemeni(email_data["subject"], email_chain_text, rules) if email_chain_text else ("Unknown", "Unknown", "0")
            primary_email_result = classify_email_gemeni(email_data["subject"], email_body_text, rules)

            # 2. Confidence Score Comparison:
            document_confidence = float(document_result[2])
            email_chain_confidence = float(email_chain_result[2])
            primary_email_confidence = float(primary_email_result[2])

            primary_result  = primary_email_result  # Default to email body
            if document_confidence > primary_email_confidence and document_confidence > email_chain_confidence:
                primary_result  = document_result
            elif email_chain_confidence > primary_email_confidence and email_chain_confidence > document_confidence:
                primary_result  = email_chain_result

        # Extract classification results
        request_type = primary_result[0]
        sub_request_type = primary_result[1]
        confidence_score = primary_result[2]

        duplicate_flag, duplicate_reason = check_duplicate(email_data["body"])
        email_obj = {
            "sender": email_data["sender"],
            "subject": email_data["subject"],
            "request_type": request_type,
            "sub_request_type": sub_request_type,
            "confidence_score": confidence_score,
            "duplicate_flag": duplicate_flag,
            "extracted_numbers_list": all_extracted_numbers
        }
        return email_obj
    else:
        print(f"Parsing failed for file: {filename}")
        return None
    

def load_priority_rules() -> dict:
    """
    Loads the priority rules from a JSON file.
    The JSON file should be located at 'config/rules.json'.
    If the file does not exist, a default rules dictionary is returned.
    
    Expected JSON structure example:
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
        }
      }
    }
    """
    # Get the rules directory and filename from environment variables
    RULES_FILENAME =  settings.settings.ALLOWED_PRIORITY_RULES_FILENAME
    RULES_DIR = Path("data/attachments")
    # Build the full file path using pathlib
    RULES_FILE_PATH = Path(RULES_DIR) / RULES_FILENAME
    
    if os.path.exists(RULES_FILE_PATH):
        with open(RULES_FILE_PATH, "r") as file:
            return json.load(file)
    
    # Return default rules if file doesn't exist
    return {
        "priority_rules": {
            "is_prioritization_extraction": False,
            "request_type_identification": {
                "order": ["email_content", "document_content"],
                "fallback": "document_content"
            },
            "numerical_field_extraction": {
                "preferred_source": ["attachments"],
                "fallback": "email_body"
            }
        }
    }