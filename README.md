# Chatbot Application

This project is a chatbot application built using Flask and OpenAI's GPT-3.5-turbo model. The chatbot can classify user queries, fetch relevant data, and provide responses based on the context.

## Features

- User-friendly chat interface
- Query classification using GPT-3.5-turbo
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
│   │   └── docx.py
│   │   └── ocr.py
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
└── index.py
└── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
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
    flask run
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

- Open your browser and navigate to `http://127.0.0.1:5000/` to access the chatbot interface.
- Type your message in the input box and click "Send" to interact with the chatbot.

## API Endpoints

- **POST /chat**: Send a message to the chatbot.
- **POST /reset**: Reset the conversation context.
- **GET /**: Render the chatbot interface.