# ---------- Base Image ----------
FROM python:3.11-slim

# set workdir
WORKDIR /app

# prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# install system deps
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# expose FastAPI port
EXPOSE 8000

# entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]
