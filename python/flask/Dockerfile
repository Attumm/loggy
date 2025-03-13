# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Datadog environment variables
    DD_SERVICE="loggy" \
    DD_ENV="production" \
    DD_TRACE_ENABLED=true \
    DD_LOGS_INJECTION=true \
    DD_RUNTIME_METRICS_ENABLED=true \
    DD_PROFILING_ENABLED=true

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies including Datadog tracing
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir ddtrace

# Copy project
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Add Gunicorn configuration
ENV GUNICORN_WORKERS=4
ENV GUNICORN_THREADS=2
ENV GUNICORN_TIMEOUT=120
ENV GUNICORN_KEEP_ALIVE=5


CMD ["ddtrace-run", "gunicorn", "--bind=0.0.0.0:8000", "--workers=3", "main:app"]
