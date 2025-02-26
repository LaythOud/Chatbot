from abc import ABC, abstractmethod
from typing import Optional, Dict
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
import tiktoken
from src.logger import Logger
from enum import Enum, auto
from src.config import AZURE_ENDPOINT, AZURE_API_KEY, AZURE_API_VERSION, OPENAI_API_KEY

log = Logger.get_logger()

MODELS_2_TOKEN_LIMITS: Dict[str, int] = {
    "gpt-3.5-turbo": 4000,
    "gpt-3.5-turbo-16k": 16000,
    "gpt-4": 8100,
    "gpt-4-32k": 32000,
    "gpt-4-32k-0613": 32000,
    "gpt-4-32k-0314": 32000,
}

class OpenAIType(Enum):
    """Enum representing the types of OCR implementations."""
    ChatGPT = auto()
    Azure = auto()

class OpenAI(ABC):
    """Abstract base class for OpenAI-based LLMs."""

    @abstractmethod
    def analyse(self, messages: list) -> Optional[str]:
        """Analyze the given text using the LLM."""
        pass

    @staticmethod
    def get_token_limit(model_id: str) -> int:
        """
        Get the token limit for a given model.
        Args:
            model_id (str): The model ID.
        Returns:
            int: The token limit.
        Raises:
            ValueError: If the model ID is not supported.
        """
        if model_id not in MODELS_2_TOKEN_LIMITS:
            raise ValueError(f"Unsupported model: {model_id}. Expected one of {list(MODELS_2_TOKEN_LIMITS.keys())}")
        return MODELS_2_TOKEN_LIMITS[model_id]

    @staticmethod
    def num_tokens_from_text(messages: list, model: str) -> int:
        """
        Calculate the number of tokens required to encode a text.
        Args:
            messages (str): The text to encode.
            model (str): The name of the model to use for encoding.
        Returns:
            int: The total number of tokens required.
        Example:
            message = {'role': 'user', 'content': 'Hello, how are you?'}
            model = 'gpt-3.5-turbo'
            num_tokens_from_messages(message, model)
            output: 11
        """
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = 0
        for message in messages:
            num_tokens += 4
            for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens


class ChatGPT(OpenAI):
    """Implementation of OpenAI's ChatGPT model."""

    def __init__(self, api_key: str, model: str, higher_model: str):
        """
        Initialize the ChatGPT instance.
        Args:
            api_key (str): The OpenAI API key.
            model (str): The default model to use.
            higher_model (str): The fallback model for longer texts.
        """
        self.model = model
        self.higher_model = higher_model
        openai.api_key = api_key

    @retry(stop=stop_after_attempt(3))
    def analyse(self, messages: list) -> Optional[str]:
        """
        Analyze the given text using the ChatGPT model.
        Args:
            messages (list): The text to analyze.
        Returns:
            Optional[str]: The analysis result, or None if an error occurs.
        """
        try:
            model = (
                self.model
                if self.num_tokens_from_text(messages, self.model) * 2 <= self.get_token_limit(self.model)
                else self.higher_model
            )

            log.info(f"Using model: {model}")

            response = openai.ChatCompletion.create(
                model=model,
                 messages=messages,
                temperature=0.0
            )
            return response.choices[0].message.content
        except Exception as e:
            log.debug(f"Error analyzing text: {e}")
            return None


class Azure(OpenAI):
    """Implementation for Azure-based OpenAI."""

    def __init__(self, api_key: str, model: str, higher_model: str, api_version: str, endpint: str):
        """
        Initialize the Azure instance.
        Args:
            api_key (str): The OpenAI API key.
            model (str): The default model to use.
            higher_model (str): The fallback model for longer texts.
        """

        self.model = model
        self.higher_model = higher_model
        self.client = openai.AzureOpenAI(
            azure_endpoint = endpint,
            api_key = api_key,
            api_version = api_version,
        )


    @retry(stop=stop_after_attempt(3))
    def analyse(self, messages: list) -> Optional[str]:
        """
        Analyze the given text using Azure's OpenAI service.
        Args:
            messages (list): The text to analyze.
        Returns:
            Optional[str]: The analysis result, or None if an error occurs.
        """
        try:
            model = (
                self.model
                if self.num_tokens_from_text(messages, self.model) * 2 <= self.get_token_limit(self.model)
                else self.higher_model
            )

            log.info(f"Using model: {model}")

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.0
            )

            return response.choices[0].message.content
        except Exception as e:
            log.debug(f"Error analyzing text: {e}")
            return None
        

class OpenAIFactory:
    """Factory class to create OCR instances."""

    @staticmethod
    def create_model(model_type: OpenAIType, model: str, higher_model: str) -> Optional[OpenAI]:
        """Create an OCR instance based on the type."""
        if model_type == OpenAIType.Azure:
            return Azure(AZURE_API_KEY, model, higher_model, AZURE_API_VERSION, AZURE_ENDPOINT)
        elif model_type == OpenAIType.ChatGPT:
            return ChatGPT(OPENAI_API_KEY, model, higher_model)
        else:
            log.debug(f"Unsupported OCR type: {model_type}")
            return None