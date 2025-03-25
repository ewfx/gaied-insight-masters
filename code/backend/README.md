# 📧 Email Classification & Data Extraction Application

This application provides a streamlined solution for managing and understanding email data. It allows users to classify emails and extract relevant information through two primary methods: uploading email files directly or processing emails located in a pre-configured server directory. The results of the classification are displayed in an easy-to-read grid format.
---

## 🚀 Tech Stack
- **Python** (Backend Development)
- **FastAPI** (API Framework)
- **Uvicorn** (ASGI Server)
- **Scikit-learn & Pandas** (Data Processing)

---

## 📥 Installation & Setup
Follow these steps to set up the project on your local machine:

### BACKEND API
### 1️⃣ Clone the Repository for Backend API
```sh
 [git clone https://github.com/your-username/gen_ai_email_processing.git](https://github.com/ewfx/gaied-insight-masters.git)
 cd gaied-insight-masters\code\backend
```

### 2️⃣ Create a Virtual Environment
```sh
 python -m venv backend_env
 backend_env\Scripts\activate    # On Windows
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
- Open **Swagger UI**: [http://127.0.0.1:8000/docs]
---

## 📬 API Endpoints
| Method |     Endpoint              | Description              |
|--------|---------------------------|--------------------------|
| POST   | `/process-emails-uploadl` | Upload and process email |
| GET    | `/process-email-directory`| process email on go      |

---

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

## 📝 Contributing
Feel free to fork and contribute to this project! 😊

