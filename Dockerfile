# Use official Python image (lighter and better than raw Ubuntu)
FROM python:3.10-slim

# Install compilers and JDK
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (documentation purpose)
EXPOSE 10000

# Start FastAPI using Render's dynamic PORT
CMD uvicorn main:app --host 0.0.0.0 --port $PORT