# FROM python:3.9-slim

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["flask", "run", "--host=0.0.0.0"]


# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    # && apt-get install -y gcc libpq-dev curl netcat \
    && apt-get install -y gcc libpq-dev curl netcat-openbsd \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Default command for the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
