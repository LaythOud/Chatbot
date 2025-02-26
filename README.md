# Chatbot Application

This project is a chatbot application built using Flask and OpenAI's GPT model. The chatbot can classify user queries, fetch relevant data, and provide responses based on the context.

## Features

- User-friendly chat interface
- Query classification using GPT
- Contextual conversation handling
- CV analysis and storage
- Query matching with candidate data

## Project Structure

```
chatbot/
├── src/
│   ├── context/
│   │   └── chatbot_manager.py
│   ├── processing/
│   │   ├── docx.py
│   │   ├── ocr.py
│   ├── llm/
│   │   └── openai_llm.py
│   ├── services/
│   │   ├── cv_analyse.py
│   │   └── query.py
│   ├── views/
│   │   └── chatbot.py
│   ├── database.py
│   ├── models.py
│   ├── config.py
│   ├── logger.py
│   └── __init__.py
├── templates/
│   └── index.html
├── tests/
│   └── test_chatbot.py
└── index.py
└── requirements.txt
└── README.md
```

## OCR Approaches

This project provides multiple OCR implementations for extracting text from PDFs:

1. **SuryaOCR** (uses Surya for OCR):
   - More advanced but not supported on all machines.
   - Converts PDFs to images and applies Surya OCR.

2. **PyOCR** (uses PyPDF and Tesseract):
   - First attempts text extraction using PyPDF.
   - Falls back to Tesseract OCR if extraction fails.

*Recommended Python version: 3.13.*

## Docx Handling Approaches

This project provides two different approaches for handling DOCX files:

1. **PyDocx (python-docx)**:
   - Reads DOCX files and extracts text using `python-docx`.
   - Best suited for structured DOCX files with clear paragraph structures.

2. **UnstructuredDocx (unstructured)**:
   - Uses the `unstructured` library for extracting text.
   - More powerful when dealing with complex document layouts.

## Setup Instructions

1. **Clone the repository:**
    ```sh
    git clone https://github.com/LaythOud/Chatbot.git
    cd chatbot
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```
    SECRET_KEY=<your_secret_key>
    AZURE_API_KEY=<your_azure_api_key>
    AZURE_ENDPOINT=<your_azure_endpoint>
    AZURE_API_VERSION=<your_azure_api_version>
    OPENAI_API_KEY=<your_openai_api_key>
    ```

5. **Install dependencies**:
    ```bash
    sudo apt-get install poppler-utils
    sudo apt-get install tesseract-ocr
    ```

6. **Run the application:**
    ```sh
    python3 index.py
    ```

## Docker Setup Instructions

1. **Build the Docker image:**
    ```sh
    docker build -t chatbot-app .
    ```

2. **Run the Docker container:**
    ```sh
    docker run -d -p 5000:5000 --env-file .env chatbot-app
    ```

## Usage

- Open your browser and navigate to `http://127.0.0.1:5000/chatbot/` to access the chatbot interface.
- Type your message in the input box and click "Send" to interact with the chatbot.

## API Endpoints

- **POST /chatbot/chat**: Send a message to the chatbot.
- **POST /chatbot/reset**: Reset the conversation context.
- **GET /chatbot/**: Render the chatbot interface.

## Running Tests

To run the unit tests for the chatbot routes, use the following command:

```sh
python -m unittest discover -s tests
```