FROM ubuntu:22.04

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    gcc \
    g++ \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]