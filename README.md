![Visual-content](./data/asset/Screenshot%202025-03-09%20at%2012.35.10%E2%80%AFPM.png)
![Visual-content](./data/asset/Screenshot%202025-03-09%20at%2012.35.30%E2%80%AFPM.png)
![Visual-content](./data/asset/Screenshot%202025-03-09%20at%2012.36.39%E2%80%AFPM.png)

# Abstract

This project is a chatbot application built using Flask and OpenAI's GPT model. The chatbot can analyze CVs (PDF, DOCX) and store them in the database, classify user queries, fetch relevant data, and provide responses based on the context.

## Features

- User-friendly chat interface
- Query classification using GPT
- Contextual conversation handling
- CV analysis and storage
- Query matching with candidate data

# Methodology

## OCR Approaches

This project provides multiple OCR implementations for extracting text from PDFs:

1. **SuryaOCR** [(uses Surya for OCR)](https://github.com/VikParuchuri/surya):
   - More advanced but not supported on all machines.
   - Converts PDFs to images and applies Surya OCR.

2. **PyOCR** (uses [PyPDF](https://pypdf.readthedocs.io/en/stable/) and [Tesseract](https://github.com/tesseract-ocr/tesseract)):
   - First attempts text extraction using PyPDF.
   - Falls back to Tesseract OCR if extraction fails.

![OCR Approaches](data/assets/ocr_approaches.png)

## Docx Handling Approaches

This project provides two different approaches for handling DOCX files:

1. **PyDocx [(python-docx)](https://python-docx.readthedocs.io/en/latest/)**:
   - Reads DOCX files and extracts text using `python-docx`.
   - Best suited for structured DOCX files with clear paragraph structures.

2. **UnstructuredDocx [(unstructured)](https://github.com/Unstructured-IO/unstructured)**:
   - Uses the `unstructured` library for extracting text.
   - More powerful when dealing with complex document layouts.

![Docx Handling Approaches](data/assets/docx_handling.png)

## LLM Usage

This project leverages Large Language Models (LLMs) for various tasks:

1. **Query Classification**:
   - Uses OpenAI's GPT models to classify user queries into predefined categories.
   - Helps in identifying the intent behind user queries.

2. **Response Generation**:
   - Generates responses to user queries based on the context and available data.
   - Ensures that the responses are relevant and accurate.

3. **CV Analysis**:
   - Analyzes CVs to extract structured information such as personal details, education history, work experience, skills, projects, and certifications.
   - Uses OpenAI's GPT models to process and analyze the extracted text.

![LLM Usage](data/assets/llm_usage.png)

The project provides two implementations for LLMs:

1. **ChatGPT**:
   - Uses OpenAI's ChatGPT model for text analysis and response generation.
   - Suitable for general-purpose text processing tasks.

2. **Azure OpenAI**:
   - Provides additional flexibility and integration with Azure services.

## Dataset

The dataset for this project can include any PDF or DOCX files containing CVs. Follow the instructions in [Step 6 of the Setup Instructions](#setup-instructions) to add the dataset.

### Description

- **Size**: The dataset can vary in size depending on the number of CVs provided. It is recommended to have a diverse set of CVs to test the chatbot's capabilities effectively.
- **Scope**: The dataset should cover a wide range of industries, job roles, and experience levels to ensure comprehensive testing.
- **Characteristics**: The CVs should include various sections such as personal information, education history, work experience, skills, projects, and certifications.
- **Structure**: The dataset should be structured in a way that each CV is a separate PDF or DOCX file. 
- **Rationale for Selection**: The dataset is selected to test the chatbot's ability to analyze and extract information from CVs accurately. It helps in evaluating the performance of the OCR and LLM components.

## Limitations

This project provides a simple implementation to showcase how AI can assist in HR recruitment process. However, there are several limitations that need to be addressed for a more robust solution:

1. **Classification Categories**:
   - The current implementation uses a limited set of predefined categories for query classification.
   - There is a need to expand these categories to cover a wider range of HR-related queries.

2. **Model Support**:
   - The project currently supports only a few models (ChatGPT and Azure OpenAI).
   - Future improvements should include support for different types of models and provide a comparison between them to choose the best fit for specific tasks.

3. **Accuracy and Performance**:
   - The accuracy of query classification and response generation can be improved by fine-tuning the models and using more advanced techniques.
   - Performance optimization is also required to handle large volumes of data efficiently.

4. **Simple UI**:
   - The current user interface is basic and primarily serves to demonstrate the AI agent's capabilities.
   - Future improvements should focus on enhancing the UI for better user experience and functionality.

# Prompts

## 1. **Analyze the CV**

You are an AI CV analysis assistant. Your task is to extract structured information from CVs and format the output as shown in the example below. Follow these instructions carefully:

### Instructions
1. **Input**: You will be given the content of a candidate's CV.
2. **Output**: Return the extracted information in the exact JSON format shown below. Do not deviate from this format.
3. **Language**: Always output in english.
4. **Steps**:
   - Carefully analyze the CV content section by section.
   - Extract and structure the following information:
     - **Personal Information**: Name, email, phone, LinkedIn, GitHub, address, and any other relevant contact details.
     - **Education History**: Institution name, start date, end date (or "current"), degree, and field of study.
     - **Work Experience**: Company name, job title, start date, end date (or "current"), and job description. Sort work experience from newest to oldest.
     - **Skills**: List all skills mentioned in the CV, including technical and soft skills.
     - **Projects**: Extract projects listed in a dedicated "Projects" section (do not include projects mentioned under work experience).
     - **Certifications**: List all certifications mentioned in the CV.
5. **Rules**:
   - If a field is missing or unclear, leave it as an empty string (`""`).
   - Use "current" for ongoing roles or education.
   - Always use the date format yyyy-mm-dd. If only the year is available, use yyyy. If only the year and month are available, use yyyy-mm.
   - Be consistent with the JSON structure and keys.
   - Ensure the output is valid JSON not a markdown. Do not include any additional text or explanations. Do not include **\n** or **`**.


### Example Input

John Doe
Email: john.doe@example.com | Phone: +1 234 567 890
LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe
Summary : Experienced Python Developer with +5 years of developing high performance applications. 

Education:
- Bachelor of Science in Computer Science, University of XYZ, 2018-2022
- Master of Science in Data Science, University of ABC, 2022-current

Work Experience:
- Software Engineer, Company A, 2022-current
  - Developed scalable web applications using Python and React.
- Data Analyst Intern, Company B, 2021-2022
  - Analyzed large datasets and created visualizations using Tableau.

Skills:
- Programming: Python, JavaScript, SQL
- Tools: Git, Docker, Tableau
- Soft Skills: Communication, Teamwork

Projects:
- Personal Portfolio Website
  - Built a responsive portfolio website using React and Node.js.
- Data Analysis Dashboard
  - Created a dashboard for real-time data visualization.

Certifications:
- AWS Certified Solutions Architect
- Google Data Analytics Professional Certificate

### Example Output

{
  "personal-information": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "Summary": "Experienced Python Developer with +5 years of developing high performance applications."
    "phone": "+1 234 567 890",
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe",
    "address": ""
  },
  "education-history": [
    {
      "institution": "University of XYZ",
      "start_date": "2018-01-01",
      "end_date": "2022-12-31",
      "degree": "Bachelor of Science",
      "field_of_study": "Computer Science"
    },
    {
      "institution": "University of ABC",
      "start_date": "2022-01-01",
      "end_date": "current",
      "degree": "Master of Science",
      "field_of_study": "Data Science"
    }
  ],
  "work-experience": [
    {
      "company": "Company A",
      "start_date": "2022-01-01",
      "end_date": "current",
      "title": "Software Engineer",
      "description": "Developed scalable web applications using Python and React."
    },
    {
      "company": "Company B",
      "start_date": "2021-01-01",
      "end_date": "2022-12-31",
      "title": "Data Analyst Intern",
      "description": "Analyzed large datasets and created visualizations using Tableau."
    }
  ],
  "skills": [
    "Python",
    "JavaScript",
    "SQL",
    "Git",
    "Docker",
    "Tableau",
    "Communication",
    "Teamwork"
  ],
  "projects": [
    {
      "title": "Personal Portfolio Website",
      "description": "Built a responsive portfolio website using React and Node.js."
    },
    {
      "title": "Data Analysis Dashboard",
      "description": "Created a dashboard for real-time data visualization."
    }
  ],
  "certifications": [
    "AWS Certified Solutions Architect",
    "Google Data Analytics Professional Certificate"
  ]
}

### Original Input:

{{Input}}

## 2. **Respond**

You are a CV analysis assistant. Respond to the user query based on the provided candidate CVs.

### **Instructions**
1. **Input**: You will be given:
   - Query: A query from the user.
   - Candidate's CVs: A list of candidates' CVs in JSON format.

2. **Output**:
   - Answer the user’s query based on the information available in candidates.
   - Ensure that your response is precise, structured, and easy to read.
   - If multiple candidates match, summarize relevant details for each.
   - If no relevant information is found, politely indicate that.
   - If you couldn't classify the query, respond that you cant answer this question.

3. **Language**:
   - Always respond same as the Query languges .

4. **Rules**:
   - **Only provide answers based on the candidate's CVs**. Do not generate information beyond what is available.
   - **Keep responses factual and relevant** to the query.
   - **Ensure clarity** by formatting the response neatly.

### Original Input:
Query: {{user_input}}
Candidate's CVs: {{candidates}}

# Setup Instructions

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
    If using an **Azure endpoint**, no code changes are needed.

    If using **OpenAI**, update the model type in your code whenever you see the following snippet:
    ```python
    model = openai_llm.OpenAIFactory.create_model(  
       openai_llm.OpenAIType.Azure, "gpt-3.5-turbo", "gpt-3.5-turbo-16k"  
     )  
    ```
 Replace `openai_llm.OpenAIType.Azure` with `openai_llm.OpenAIType.ChatGPT.`

5. **Install dependencies**:
    
    `linux`

    ```bash
    sudo apt-get install poppler-utils
    sudo apt-get install tesseract-ocr
    ```

    `mac`

    ```sh
    brew install poppler
    brew install tesseract
    ```

6. **Add PDF and DOCX Files**
    Copy all PDF and DOCX files into the `data/sample_cvs` folder in the project's root directory. If the folder does not exist, create it.

7. **Run the application:**
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
    docker run -d -p 5000:5000 chatbot-app
    ```

## Usage

- Open your browser and navigate to `http://127.0.0.1:5000/chatbot/` to access the chatbot interface.
- Type your message in the input box and click "Send" to interact with the chatbot.

## API Endpoints

- **POST /chatbot/chat**: Send a message to the chatbot.
- **POST /chatbot/reset**: Reset the conversation context.
- **GET /chatbot/**: Render the chatbot interface.

## Contact Information

For any questions or support, please contact the maintainers:

- **Email**: laythoud6@gmail.com
- **GitHub**: [https://github.com/LaythOud/Chatbot](https://github.com/LaythOud/Chatbot)