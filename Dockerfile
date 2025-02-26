FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    build-essential

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "index.py"]
