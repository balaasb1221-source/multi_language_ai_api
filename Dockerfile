# Use official Python image
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install compilers and runtimes
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ default-jdk php golang kotlin r-base mono-mcs mono-runtime curl wget build-essential \
    libssl-dev libcurl4-openssl-dev libxml2-dev unzip git && \
    rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /app

# Persistent temp folder for code execution
RUN mkdir -p /tmp/code_runner && chmod -R 777 /tmp/code_runner

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 10000

# Run FastAPI with 1 worker for stability
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--workers", "1"]