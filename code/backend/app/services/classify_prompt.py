import requests
import json
from app.models.request_type_model import RequestTypeModel
from config import settings

MODEL_NAME = settings.settings.MODEL_NAME  # e.g., "tiiuae/falcon-7b-instruct"
HF_TOKEN = settings.settings.HUGGINGFACE_API_TOKEN  # Hugging Face token

if not HF_TOKEN or HF_TOKEN == "YOUR_HUGGINGFACE_API_TOKEN":
    print("Error: Hugging Face API token is missing. Please ensure you have a valid config.")
    exit()

API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_NAME}/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

PROMPT_OBJECTIVE_CLASSIFICATION_RULES = """
### Task: Email Classification 

#### **Objective:** 
Analyze the given email and classify it into the most appropriate **Request Type** and **Sub Request Type** based on its primary intent.

#### **Instructions:**
- Identify the key intent of the email.
- Match it with one of the **Request Types** from the predefined categories.
- Select the most relevant **Sub Request Type** for the classification.
- If no exact match is found, choose the closest category.

Only return a JSON object with the classification results.
"""
PROMPT_CATEGORIES = f"""
#### **Classification Categories & Definitions:** 
{json.dumps(RequestTypeModel.requests_datasets, indent=2)}
"""

PROMPT_OUTPUT_FORMAT = """
#### **Output Format:** 
Return the classification result in **pure JSON format** (without extra text or markdown).

Example Output:
{
  "request_type": "Commitment Change",
  "sub_request_type": "Increase",
  "confidence_score": 0.95,
  "email_subject": "Request for Credit Line Increase"
}
"""
PROMPT_TEMPLATE = """ 
### Task: Email Classification  
#### **Objective:**  
Analyze the given email and classify it into the most appropriate **Request Type** and **Sub Request Type** based on its primary intent. Ensure the response is strictly in JSON format with the specified fields.  

#### **Classification Categories:**  
Each email must be categorized under one of the following **Request Types** and corresponding **Sub Request Types**:  

| Request Type              | Sub Request Type                                      |  
|---------------------------|------------------------------------------------------|  
| Adjustment                | N/A                                                  |  
| AU Transfer               | N/A                                                  |  
| Closing Notice            | Reallocation Fees, Amendment Fees, Reallocation Principal |  
| Commitment Change         | Cashless Roll, Decrease, Increase                    |  
| Fee Payment               | Ongoing Fee, Letter of Credit Fee                    |  
| Money Movement - Inbound  | Principal, Interest, Principal + Interest, Principal + Interest + Fee |  
| Money Movement - Outbound | Timebound, Foreign Currency                          |  

#### **Output Format:**  
Return the classification result strictly in **JSON format** with the following fields:  
```json
{
  "request_type": "Request Type",
  "sub_request_type": "Sub Request Type",
  "confidence_score": Confidence Score (between 0 and 1),
  "email_subject": "Email Subject"
}
### **🔹 Email for Classification:**  
```email
{{
QQA Bank, N.A.
Loan Agency Services


 Date: 05-Feb-2025
    TO: ABC BANK, NATIONAL ASSOCIATION
ATTN: RAMAKRISHNA KUNCHALA
    Fax: 877-606-9426
      Re: ABB MID-ATLANTIC LLC $171.3MM 11-4-2022, TERM LOAN A-2

Description: Facility Lender Share Adjustment

BORROWER: ABB MID-ATLANTIC LIC
DEAL NAME: ABB MID-ATLANTIC LIC $171. 3MM 11-4-2022

Effective 04-Feb-2025, the Lender Shares of facility TERM LOAN A-2 have been adjusted.
Your share of the commitment was USD 5,518,249.19. It has been Increased to USD 5,542,963.55.

For: ABC BANK, NA

Reference: ABIB MID-ATLANTIC LIC $171.3MM 11-4-2022,

If you have any questions, please call the undersigned.
********************************************COMMENT***************************************
PLEASE FUND YOUR SHARE OF $24,714.36


Bank Name: QQA Bank NA
ABA   #   011500120
Account #: 0026693011
Account Name: LIQ CLO Operating Account
Ref: ABTB Mid-Atlantic LLC

********************************************************************************************
Regards,

SCOTT WALLACE
Telephone #:
Fax #:

QQA Commercial Banking is a brand name of QQA Bank, N.A. Member FDIC

}}

"""

def extract_json_from_response(response_text):
    """Extract JSON response from model output."""
    try:
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_string = response_text[json_start:json_end]
        return json.loads(json_string)
    except (ValueError, json.JSONDecodeError):
        return {"error": "Could not extract JSON from model output"}

def send_to_huggingface_api(prompt):
    """Send the prompt to Hugging Face API and get the response."""
    try:
        payload = {
            "messages": [
                {"role": "system", "content": PROMPT_OBJECTIVE_CLASSIFICATION_RULES + PROMPT_CATEGORIES + PROMPT_OUTPUT_FORMAT},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 700,
            "temperature": 0.2,
            "top_p": 0.8,
            "model": MODEL_NAME
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"]
        return {"error": "Unexpected API response format"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}


def classify_email_with_prompt(email_text):


    final_response = send_to_huggingface_api(email_text)
    
    try:
        classification = extract_json_from_response(final_response)
        request_type = classification.get("request_type", "").strip()
        if request_type:
            valid_sub_types = RequestTypeModel.get_sub_types(request_type)
            sub_request_type = classification.get("sub_request_type", "").strip()
            if sub_request_type not in valid_sub_types:
                classification["sub_request_type"] = valid_sub_types[0]
        return classification
    except Exception as e:
        return {"error": str(e)}

# Example Usage
if __name__ == "__main__":
    email_text = """
    QQA Bank, N.A.
    Loan Agency Services
    Date: 05-Feb-2025
    Description: Facility Lender Share Adjustment
    """
    classification = classify_email_with_prompt(email_text)
    print(classification)
