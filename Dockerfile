# Use official Python image (slim version)
FROM python:3.10-slim

# Install compilers, JDK, and PHP
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    php-cli \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for documentation / Render)
EXPOSE 10000

# Start FastAPI using Render's dynamic PORT environment variable
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]