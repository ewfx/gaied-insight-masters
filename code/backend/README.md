# 📧 Gen AI Email Processing

This project is an AI-powered email processing system that reads, extracts, classifies, and analyzes emails and documents using LLaMA models. It supports OCR for images/PDFs and utilizes machine learning to classify emails.

---

## 🚀 Tech Stack
- **Python** (Backend Development)
- **FastAPI** (API Framework)
- **PyTorch & Transformers** (AI Model - LLaMA)
- **OCR Tools** (Tesseract, pdfplumber, python-docx)
- **Langchain & Sentence-Transformers** (Text Processing & Embeddings)
- **Uvicorn** (ASGI Server)
- **Scikit-learn & Pandas** (Data Processing)
- **LLama-CPP-Python** (LLaMA Model Integration)

---

## 📥 Installation & Setup
Follow these steps to set up the project on your local machine:

### 1️⃣ Clone the Repository
```sh
 git clone https://github.com/your-username/gen_ai_email_processing.git
 cd gen_ai_email_processing
```

### 2️⃣ Create a Virtual Environment
```sh
 python -m venv env
 source env/bin/activate  # On macOS/Linux
 env\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies
```sh
 pip install --upgrade pip
 pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI Server
```sh
 uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5️⃣ Access the API Documentation
- Open **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- Open **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📬 API Endpoints
| Method | Endpoint          | Description              |
|--------|------------------|--------------------------|
| POST   | `/upload-email`  | Upload and process email |
| GET    | `/health`        | Check API status         |

---

## 🛠 Environment Variables
Create a `.env` file in the **config/** directory and add the necessary settings:
```ini
MODEL_PATH=/path/to/llama/model
OCR_LANGUAGE=eng
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

## 📝 Contributing
Feel free to fork and contribute to this project! 😊

