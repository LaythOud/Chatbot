FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "index.py"]
