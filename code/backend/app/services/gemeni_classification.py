import google.generativeai as genai
import json
import email
import io
import PyPDF2
import docx
import mimetypes
   

genai.configure(api_key="AIzaSyBdZsC0DG4OYjitl-OmFHLVqYOrBSFkV-c")

# model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel("gemini-2.0-flash-lite")

classification_categories = [
    {"request_type": "Adjustment", "sub_request_types": ["N/A"]},
    {"request_type": "AU Transfer", "sub_request_types": ["N/A"]},
    {"request_type": "Closing Notice", "sub_request_types": ["Reallocation Fees", "Amendment Fees", "Reallocation Principal"]},
    {"request_type": "Commitment Change", "sub_request_types": ["Cashless Roll", "Decrease", "Increase"]},
    {"request_type": "Fee Payment", "sub_request_types": ["Ongoing Fee", "Letter of Credit Fee"]},
    {"request_type": "Money Movement - Inbound", "sub_request_types": ["Principal", "Interest", "Principal + Interest", "Principal + Interest + Fee"]},
    {"request_type": "Money Movement - Outbound", "sub_request_types": ["Timebound", "Foreign Currency"]},
    {"request_type": "Account Opening", "sub_request_types": ["Checking Account", "Savings Account", "Money Market Account", "Certificate of Deposit (CD)"]},
    {"request_type": "Account Closing", "sub_request_types": ["Checking Account", "Savings Account", "Money Market Account", "Certificate of Deposit (CD)"]},
    {"request_type": "Balance Inquiry", "sub_request_types": ["Checking Account", "Savings Account", "Loan Account", "Credit Card Account"]},
    {"request_type": "Statement Request", "sub_request_types": ["Checking Account", "Savings Account", "Loan Account", "Credit Card Account"]},
    {"request_type": "Transaction History Request", "sub_request_types": ["Checking Account", "Savings Account", "Loan Account", "Credit Card Account"]},
    {"request_type": "Funds Transfer", "sub_request_types": ["Internal Transfer", "External Transfer (ACH, Wire)"]},
    {"request_type": "Stop Payment", "sub_request_types": ["Check", "Electronic Transfer"]},
    {"request_type": "Credit Card Application", "sub_request_types": ["Personal", "Business"]},
    {"request_type": "Credit Limit Change", "sub_request_types": ["Increase", "Decrease"]},
    {"request_type": "Loan Application", "sub_request_types": ["Mortgage", "Auto Loan", "Personal Loan", "Business Loan"]},
    {"request_type": "Loan Disbursement", "sub_request_types": ["Initial Disbursement", "Subsequent Disbursement"]},
    {"request_type": "Loan Payoff", "sub_request_types": ["Principal", "Interest", "Fees"]},
    {"request_type": "Customer Information Update", "sub_request_types": ["Address Change", "Phone Number Change", "Email Address Change"]},
    {"request_type": "Online/Mobile Banking Access", "sub_request_types": ["Enrollment", "Password Reset", "Access Removal"]},
    {"request_type": "Security Request", "sub_request_types": ["Change PIN", "Report Lost/Stolen Card", "Fraud Alert"]}
]


def extract_text_from_attachment(attachment_bytes, filename):
    file_type, _ = mimetypes.guess_type(filename)

    if file_type == 'application/pdf':
        try:
            pdf_file = io.BytesIO(attachment_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        try:
            doc = docx.Document(io.BytesIO(attachment_bytes))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting Word: {e}")
            return ""
    else:
        try:
            return attachment_bytes.decode('utf-8')
        except UnicodeDecodeError:
            print("Unsupported attachment type or encoding.")
            return ""
        

def extract_text_from_email(email_string):
    try:
        msg = email.message_from_string(email_string)
        text = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text += part.get_payload(decode=True).decode()
            elif part.get_content_type() == "text/html":
                #basic html removal, for more robust html, use BeautifulSoup.
                html = part.get_payload(decode=True).decode()
                text += ''.join(c if ord(c) < 128 else ' ' for c in html.replace("<br>", "\n").replace("<p>", "\n").replace("</p>","\n").replace("<div>","\n").replace("</div>","\n").replace("<span>"," ").replace("</span>", " "))

        return text
    except Exception as e:
        print(f"Error parsing email: {e}")
        return ""

def analyze_intent(text):
    prompt = f"Analyze the following text: {text}. What is the primary intent?"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API error (Intent): {e}")
        return ""


def classify_email_gemeni(subject, body):
    """Classifies an email based on request type and sub-request type."""
    results = []
    categories_string = str(classification_categories)
    PROMPT = f"""
    Analyze the following email and classify it into the most appropriate Request Type and Sub Request Type based on its primary intent.

    Classification Categories:
    {categories_string}

    Email Subject: {subject}
    Email Content: {body}

    Output Format:
    {{
        "request_type": "Request Type",
        "sub_request_type": "Sub Request Type",
        "confidence_score": "Confidence Score (between 0 and 1)",
    }}
    """
   

    
    response = model.generate_content(PROMPT)

    if response and hasattr(response, "_result"):
        text_response = response._result.candidates[0].content.parts[0].text
        text_response = text_response.strip().replace("```json", "").replace("```", "").strip()
        try:
            parsed_json = json.loads(text_response)

            request_type = parsed_json.get("request_type", "Unknown")
            sub_request_type = parsed_json.get("sub_request_type", "Unknown")
            confidence_score = parsed_json.get("confidence_score", "Unknown")

            results.extend([request_type,sub_request_type,confidence_score])
            return results

        except json.JSONDecodeError as e:
            print(f"Exception during JSON Parsing: {e}")
    else:
        print("We did not get response.")




def get_primary_intent(email_content, attach_content):
    """Detects primary intent when multiple requests are present."""

    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    prompt = f"""
    Analyze the following email and document, and determine which one has the primary intent. 
    email::{email_content} 
    document: {attach_content}
    """
    response = model.generate_content(prompt)
    return response.text  # Extracted primary intent



