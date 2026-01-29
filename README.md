Nice — let’s extend this with **Celery + Redis worker setup**, keeping it beginner-friendly.

---

# 🚀 FastAPI Hospital Bulk Processor — Setup & Run Guide

This project is a FastAPI-based backend service for bulk hospital processing using **FastAPI + Redis + Celery workers**.

---

## 📦 1. Prerequisites

Make sure you have:

* **Python 3.9+**
* **pip**
* **Redis** (local or hosted like Render)
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

# Redis (used for Celery + batch datastore)
REDIS_URL=redis://localhost:6379/0
```

If using **Render Redis**, paste the internal Redis URL here.

---

## 🧠 6. Start Redis (Local Only)

If running locally:

**Mac**

```bash
brew install redis
brew services start redis
```

**Linux**

```bash
sudo service redis-server start
```

Check Redis:

```bash
redis-cli ping
```

Should return:

```
PONG
```

---

## ▶️ 7. Run FastAPI Application

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 👷 8. Start Celery Worker (IMPORTANT)

Open **another terminal** (same virtualenv).

Run:

```bash
celery -A app.queue.celery_app.celery_app worker --loglevel=info --concurrency=4
```

### What this does

* Starts background workers
* Processes bulk upload jobs
* Reads tasks from Redis
* Updates batch status

If worker is running correctly, you’ll see logs like:

```
[tasks]
  . app.tasks.bulk_tasks.process_bulk_task
```

---

## 📚 9. API Documentation

FastAPI automatically provides docs:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## ❤️ Health Check

```http
GET /health
```

---

## 📊 Metrics Endpoint

Prometheus metrics available at:

```
GET /metrics
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

## 🧩 How System Works

1. CSV uploaded → API validates
2. API enqueues job to **Redis queue**
3. Celery worker picks job
4. Worker processes hospitals in parallel
5. Batch status stored in Redis
6. Client checks status via `/hospitals/bulk/{batch_id}`

---

## 🛑 Common Issue

If uploads don’t process:

- ✔ Check Redis is running
- ✔ Check Celery worker is running
- ✔ Check REDIS_URL is correct

---
