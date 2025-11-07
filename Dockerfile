# Dockerfile for Railway deployment
# This adds WeasyPrint system dependencies to your existing Railway setup
# Railway will use this for building, but Procfile will still control the start command

FROM python:3.11-slim

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Railway will use Procfile for start command, but we set a default here
# Procfile: web: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 --log-level info
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:${PORT:-5000}", "--workers", "2", "--threads", "4", "--timeout", "60", "--log-level", "info"]

