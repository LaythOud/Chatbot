from src.logger import Logger
from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum, auto
from docx import Document
from unstructured.partition.docx import partition_docx

log = Logger.get_logger()

class DocxType(Enum):
    """Enum representing the types of Docx implementations."""
    PYDOCX = auto()
    UNSTRUCTURED = auto()

class Docx(ABC):
    """Abstract base class for docx implementations."""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    @abstractmethod
    def extract_text(self) -> Optional[str]:
        """Extract text from the Docx file."""
        pass

class PyDocx(Docx):
    """Docx implementation using python-docx."""

    def extract_text(self) -> Optional[str]:
        """Extract text using python-docx."""
        try:
            log.info(f"Extracting text from {self.pdf_path} using python-docx.")
            docx = Document(self.pdf_path)
            return "\n".join([paragraph.text for paragraph in docx.paragraphs])
        except Exception as e:
            log.debug(f"Error extracting text with Surya: {e}")
            return None
        
class UnstructuredDocx(Docx):
    """Docx implementation using unstructured."""

    def extract_text(self) -> Optional[str]:
        """Extract text using unstructured."""
        try:
            log.info(f"Extracting text from {self.pdf_path} using python-docx.")
            docx = partition_docx(self.pdf_path)
            return "\n".join([paragraph.text for paragraph in docx])
        except Exception as e:
            log.debug(f"Error extracting text with Surya: {e}")
            return None

class DocxFactory:
    """Factory class to create Docx instances."""

    @staticmethod
    def create_docx(docx_type: DocxType, pdf_path: str) -> Optional[Docx]:
        """Create an OCR instance based on the type."""
        if docx_type == DocxType.PYDOCX:
            return PyDocx(pdf_path)
        elif docx_type == DocxType.UNSTRUCTURED:
            return UnstructuredDocx(pdf_path)
        else:
            log.debug(f"Unsupported Docx type: {docx_type}")
            return None