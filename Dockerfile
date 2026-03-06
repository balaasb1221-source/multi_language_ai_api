# Use official Python slim image
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install compilers and runtimes
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ default-jdk php golang-go kotlin r-base mono-mcs mono-runtime clang \
    curl wget build-essential libssl-dev libcurl4-openssl-dev libxml2-dev unzip git \
    libicu-dev libncurses5 libpython3.10 && \
    rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Swift
RUN wget https://swift.org/builds/swift-5.9.3-release/ubuntu2004/swift-5.9.3-RELEASE/swift-5.9.3-RELEASE-ubuntu20.04.tar.gz
RUN tar xzf swift-5.9.3-RELEASE-ubuntu20.04.tar.gz -C /usr/share/
ENV PATH="/usr/share/swift-5.9.3-RELEASE-ubuntu20.04/usr/bin:${PATH}"

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

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--workers", "1"]