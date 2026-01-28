Here’s a cleaner, beginner-friendly version focused on **installation + running**.

---

# 🚀 FastAPI Hospital Bulk Processor — Setup & Run Guide

This project is a FastAPI-based backend service for bulk hospital processing.

---

## 📦 1. Prerequisites

Make sure you have:

* **Python 3.9+**
* **pip**
* (Optional) **virtualenv**

Check Python version:

```bash
python --version
```

---

## 🛠️ 2. Clone the Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

## 🧪 3. Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Mac/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

---

## 📥 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ 5. Configure Environment Variables

Create a `.env` file in project root:

```env
APP_NAME=Hospital Bulk Processor
HOSPITAL_API_URL=https://hospital-directory.onrender.com
MAX_CONCURRENT_REQUESTS=5
MAX_UPLOAD_SIZE=51200
CORS_ALLOW_ORIGINS=*
```

---

## ▶️ 6. Run the Application Locally

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📚 7. API Documentation

FastAPI automatically provides docs:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## ❤️ Health Check

```bash
GET /health
```

---

## 🧪 Run Tests

```bash
pytest -v
```

With coverage:

```bash
pytest --cov=app
```

---