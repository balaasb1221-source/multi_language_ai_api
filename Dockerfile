# Use Python slim image
FROM python:3.10-slim

# Install compilers, JDK, and PHP
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    php \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your FastAPI app will run on
EXPOSE 10000

# Start FastAPI using uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]