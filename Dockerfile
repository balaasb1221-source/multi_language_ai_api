# Use official Python image (slim)
FROM python:3.10-slim

# Install compilers, JDK, wget
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    wget \
    php \
    && rm -rf /var/lib/apt/lists/*

# Install .NET SDK for C#
RUN wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y dotnet-sdk-7.0 \
    && rm packages-microsoft-prod.deb

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Render
EXPOSE 10000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]