# =========================
# Base Image
# =========================
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# =========================
# Install essential tools and compilers
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    nodejs \
    npm \
    curl \
    git \
    unzip \
    vim \
    nano \
    sudo \
    php-cli \
    golang-go \
    rustc \
    cargo \
    r-base \
    mono-mcs \
    mono-runtime \
    snapd \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# =========================
# Install Kotlin manually
# =========================
RUN apt-get update && apt-get install -y wget unzip

RUN wget https://github.com/JetBrains/kotlin/releases/download/v1.9.24/kotlin-compiler-1.9.24.zip

RUN unzip kotlin-compiler-1.9.24.zip -d /opt/

RUN ln -s /opt/kotlinc/bin/kotlinc /usr/local/bin/kotlinc

# =========================
# Set working directory
# =========================
WORKDIR /app

# =========================
# Copy Python dependencies first (for caching)
# =========================
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# =========================
# Copy the rest of the project
# =========================
COPY . /app

# =========================
# Expose API port
# =========================
EXPOSE 10000

# =========================
# Start FastAPI server
# =========================
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]