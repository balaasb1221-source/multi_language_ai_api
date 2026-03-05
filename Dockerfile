# Use official Python image
FROM python:3.10-slim

# Install compilers and runtimes
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    php \
    golang \
    kotlin \
    r-base \
    mono-mcs \
    mono-runtime \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Swift (basic version)
RUN apt-get update && apt-get install -y swiftlang || true

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 10000

# Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]