import os
from pathlib import Path
import json
from src.llm import openai_llm
from src.processing import ocr, docx
from src.database import db
from src.models import Candidate
from src.logger import Logger
from src.config import root_directory

log = Logger.get_logger()

class CVAnalyse:
    @staticmethod
    def analyse(cv_folder="/data/sample_cvs"):
        # Construct the full path to the CV folder
        cv_folder_path = Path(root_directory + cv_folder)

        # Load the base prompt for CV analysis
        prompt_base_path = os.path.join(root_directory, "src/prompts/analyze_cv.md")
        with open(prompt_base_path, "r") as file:
            prompt_base = file.read()

        # Initialize the OpenAI model
        model = openai_llm.OpenAIFactory.create_model(
            openai_llm.OpenAIType.Azure, "gpt-3.5-turbo", "gpt-3.5-turbo-16k"
        )

        results = 0

        # Iterate over all PDF files in the CV folder
        for pdf in cv_folder_path.iterdir():
            if pdf.is_file() and (pdf.suffix == ".pdf" or pdf.suffix == ".docx"):
                # Check if the file has already been processed
                if Candidate.query.filter_by(filename=pdf.name).first():
                    log.info(f"File already processed: {pdf.name}")
                    continue

                # Extract text from the PDF
                try:
                    if pdf.suffix == ".pdf":
                        text = ocr.OCRFactory().create_ocr(
                            ocr.OCRType.PYPDF, str(pdf)
                        ).extract_text()
                    else:
                        text = docx.DocxFactory().create_docx(
                            docx.DocxType.UNSTRUCTURED, str(pdf)
                        ).extract_text()
                except Exception as e:
                    log.debug(f"Error extracting text from {pdf.name}: {e}")
                    continue

                if text.strip():
                    # Prepare the prompt for the LLM
                    prompt = prompt_base.replace("{{Input}}", text)

                    # Analyze the CV text using the LLM
                    try:
                        response = model.analyse(messages=[
                            {"role": "user", "content": prompt}
                        ])
                        response = json.loads(response)
                    except Exception as e:
                        log.debug(f"Error analyzing CV {pdf.name}: {e}")
                        continue
                    
                    # Extract personal information from the response
                    personal_info = response.get("personal-information", {})

                    # Create a new CVAnalysisResult instance
                    cv_result = Candidate(
                        filename=pdf.name,  # Store the filename for uniqueness
                        candidate_name=personal_info.get("name", ""),
                        email=personal_info.get("email", ""),
                        phone=personal_info.get("phone", ""),
                        linkedin=personal_info.get("linkedin", ""),
                        github=personal_info.get("github", ""),
                        address=personal_info.get("address", ""),
                        education_history=response.get("education-history", []),
                        work_experience=response.get("work-experience", []),
                        skills=response.get("skills", []),
                        projects=response.get("projects", []),
                        certifications=response.get("certifications", [])
                    )

                    # Add the result to the database session
                    db.session.add(cv_result)
                    results += 1
                    log.info(f"Processed CV: {pdf.name}")
                else:
                    log.debug(f"No text extracted from: {pdf.name}")

        # Commit all changes to the database
        try:
            db.session.commit()
            log.info(f"Successfully analyzed and stored {results} CVs.")
        except Exception as e:
            db.session.rollback()
            log.debug(f"Error committing to the database: {e}")