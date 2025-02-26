from src.llm import openai_llm
from src.logger import Logger
import os
from src.config import root_directory
import json

log = Logger.get_logger()

class Query:
    @staticmethod
    def classify_query(user_input: str, conversation: list):
        """
        Uses LLM to classify user query into predefined categories.
        Returns: category (str)
        """
        try:
            model = openai_llm.OpenAIFactory.create_model(
                openai_llm.OpenAIType.Azure, "gpt-3.5-turbo", "gpt-3.5-turbo-16k"
            )

            prompt_base_path = os.path.join(root_directory, "src/prompts/classify_user_query.md")
            with open(prompt_base_path, "r") as file:
                prompt_base = file.read()

            prompt = prompt_base.replace("{{user_input}}", user_input)
            conversation.insert(0, {"role": "system","content": prompt})
            response = model.analyse(messages=conversation)
            
            return response.strip()
        except Exception as e:
            log.error(f"Query error: {str(e)}")
            return "OTHER"

    @staticmethod
    def response_to_query(user_input: str, conversation: list, candidates):
        """
        Uses LLM to response to user query after getting the required informations.
        Returns: response (str)
        """
        try:
            model = openai_llm.OpenAIFactory.create_model(
                openai_llm.OpenAIType.Azure, "gpt-3.5-turbo", "gpt-3.5-turbo-16k"
            )

            prompt_base_path = os.path.join(root_directory, "src/prompts/response_to_user_query.md")
            with open(prompt_base_path, "r") as file:
                prompt_base = file.read()

            prompt = prompt_base.replace("{{user_input}}", user_input).replace("{{candidates}}", json.dumps(candidates, indent=2))
            conversation.insert(0, {"role": "system","content": prompt})
            response = model.analyse(messages=conversation)
            
            return response.strip()
        except Exception as e:
            log.error(f"Query classification error: {str(e)}")
            return "OTHER"
