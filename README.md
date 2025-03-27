# 🚀 Gen AI Orchestrator for Email and Document Triage/Routing

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
This application provides a streamlined solution for managing and understanding email data. It allows users to classify emails and extract relevant information through two primary methods: uploading email files directly or processing emails located in a pre-configured server directory. The results of the classification are displayed in an easy-to-read grid format.

---

## Getting Started
## 🎥 Demo
🔗 [Live Demo ](https://genaiemailtriage.netlify.app/) (if applicable)  
📹 [Clieck me for Video Demo on drive](https://drive.google.com/file/d/1KQIDEQ24ko5qGpP3MuEjFRh-MSs6qeJK/view?usp=drive_link) (if applicable) 
📹 [Clieck me for Video Demo on Youtube](https://www.youtube.com/watch?v=UL1du2m-lD8&feature=youtu.be) (if applicable) 



---
## API Server Url

 Now, we can test the Email Processing API, which is deployed at the following link: 
[https://vivek0912-genaiemailclassification.hf.space/docs]

## Frontend UI Url
 Now, we can access frontend ui for the Email Processing which is deployed at the following link:
[https://genaiemailtriage.netlify.app]

---

## 🖼️ Test Artifacts Screenshots:

![Screenshot 1](artifacts/demo/screenshot1.png)
![Screenshot 2](artifacts/demo/screenshot2.png)
![Screenshot 3](artifacts/demo/screenshot3.png)
![Screenshot 4](artifacts/demo/screenshot4.jpg)

---
---
## Priority-Based Extraction and Key Consideration Rules JSON sample
 The system determines which source of information to prioritize when extracting data. This helps ensure accurate classification and structured extraction based 
 on predefined rules. This section provides business-specific classification rules for extracting request types and sub-request types based on document/email 
 content.This ensures that the application dynamically applies the extraction and classification rules based on the JSON configuration.
 * The JSON file can be downloaded from README.md file and can get from swagger doc, modified, and re-uploaded using API endpoints.
 * Users can configure priority rules locally and then send updates via an API request.

[sample JOSN](artifacts/arch/Priority_Extraction_Rules.json)

---

## 💡 Inspiration
What inspired you to create this project? Describe the problem you're solving.

---

---
## ⚙️ What It Does
* **Email File Upload:** Users can upload one or more email files (supporting `.eml`, `.msg`, `.txt` formats) directly through the web interface for immediate processing and classification.
* **Directory Processing:** The application can be configured to automatically process all email files within a specific server directory. This feature is ideal for handling large volumes of emails or for automated background processing.
* **Intelligent Classification:** Utilizes advanced models (potentially leveraging Gemini AI as indicated in the code) to categorize emails based on their content, subject, and attachments.
* **Data Extraction:** Extracts key information from emails, including sender, subject, and potentially other relevant data points.
* **Confidence Scoring:** Provides a confidence score for each classification, indicating the reliability of the prediction.
* **Duplicate Detection:** Identifies and flags potential duplicate emails based on their content.
* **Clear Results Display:** Presents the classification results in a user-friendly grid table, showing key information like sender, subject, predicted request type, sub-request type, confidence score, and duplicate status.
* **Loading Indicator:** Provides visual feedback during the email processing to keep users informed of the application's status.
* ** Priority based Extraction **

---
## 🛠️ How We Built It
Briefly outline the technologies, frameworks, and tools used in development.
- 🔹 Frontend: Angular
- 🔹 Backend:  FastAPI / 
- 🔹 Other: GEMINI
- 🔹 Uvicorn: (ASGI Server)
- 🔹 Scikit-learn & Pandas: (Data Processing)

---
## 🚧 Challenges We Faced
🔹 Technical Challenges
1. LLM model selection and fine-tuning were performed based on the domain to ensure more accurate results. However, I faced resource constraints due to my personal laptop’s configuration. I initially experimented with LLaMA and Falcon, but due to token limitations, I ultimately finalized the Gemini LLM models.
   
2. API Rate Limits & Quotas
Issue: The Google Gemini API has request rate limits, restricting the number of emails processed per minute.

 Solution: Implemented batch processing and cached responses to minimize API calls.

3. Handling Long Emails (Token Limit)
Issue: Gemini models have input token limits, causing issues with long emails.

Solution: Used text summarization before classification to reduce input size.

4. Model Output Variability
Issue: Gemini sometimes generates inconsistent or ambiguous classifications.

Solution: Used structured prompting and few-shot learning to improve reliability.

5. Latency in Real-Time Classification
Issue: API-based models introduce a delay in processing, especially for bulk emails.


🔹 Non-Technical Challenges
1. Understanding Business Requirements
Issue: Stakeholders had different expectations for email classification categories.

2. User Trust in AI Predictions
Issue: Some users doubted the accuracy of AI-based classification.

Solution: Provided explainability by adding confidence scores in responses.


---
## BACKEND API
## 🏃 How to Run Backend code
1. Clone the repository  
   ```sh
   git clone https://github.com/your-username/gen_ai_email_processing.git](https://github.com/ewfx/gaied-insight-masters.git)
   cd gaied-insight-masters\code\backend
   ```
2. Create a Virtual Environment
 ```sh
   python -m venv backend_env
   backend_env\Scripts\activate    # On Windows
  ```
4. Install dependencies  
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Run the project  
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
6. Access the API Documentation
    ```sh
     Open Swagger UI: [http://127.0.0.1:8000/docs]
   ```
## 📬 API Endpoints
| Method   |     Endpoint                  | Description                  |
|--------  |-------------------------------|----------------------------|
| POST     | `/process-emails-uploadl`     | Upload and process email   |
| POST     | `/process-email-directory`    | process email on go        |
| PPST     | `/api/upload-priority-rules/` | set priority rules in json |

## 🏗️ Tech Stack
- 🔹 Frontend: Angular
- 🔹 Backend:  FastAPI / 
- 🔹 LLM Model: GEMINI
- 🔹 Uvicorn: (ASGI Server)
- 🔹 Scikit-learn & Pandas: (Data Processing)
## 🛠 Environment Variables
Create a `.env` file in the **config/** directory and add the necessary settings:
```ini
MODEL_PATH=gemini-2.0-flash-lite
```
---

## 🔄 Updating the Project
If you pull new changes from GitHub, remember to update dependencies:
```sh
 git pull origin main
 pip install -r requirements.txt
```
---
## 📤 Pushing the Project to GitHub
After making changes, push them to GitHub:
```sh
 git add .
 git commit -m "Updated project files"
 git push origin main
```
---
### Frontend UI(Angular)
1. Clone the repository  
   ```sh
   git clone https://github.com/your-username/gen_ai_email_processing.git](https://github.com/ewfx/gaied-insight-masters.git)
   cd gaied-insight-masters\code\frontend
   ```
2. Install dependencies  
   ```sh
   npm install
   ```
3. Run the project  
   ```sh
   ng serve/npm start
   ```
4. Access the API Documentation
    ```sh
     Open UI: [http://localhost:4200/]
   ```

---
## 👥 Team
- **Vivek Vishal** - [GitHub](#) | [LinkedIn](#)
- **Dharmendar Potlaplli** - [GitHub](#) | [LinkedIn](#)
