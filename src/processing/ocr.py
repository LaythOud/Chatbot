import pypdf
import pytesseract
import surya
from abc import ABC, abstractmethod
from pdf2image import convert_from_path
from typing import Optional
from enum import Enum, auto
from src.logger import Logger

log = Logger.get_logger()

class OCRType(Enum):
    """Enum representing the types of OCR implementations."""
    SURYA = auto()
    PYPDF = auto()

class OCR(ABC):
    """Abstract base class for OCR implementations."""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    @abstractmethod
    def extract_text(self) -> Optional[str]:
        """Extract text from the PDF."""
        pass


class SuryaOCR(OCR):
    """OCR implementation using Surya."""

    def extract_text(self) -> Optional[str]:
        """Extract text using Surya."""
        try:
            log.info(f"Extracting text from {self.pdf_path} using Surya.")
            images = convert_from_path(self.pdf_path)
            return "\n".join([surya.ocr.run_ocr(img)["text"] for img in images])
        except Exception as e:
            log.debug(f"Error extracting text with Surya: {e}")
            return None


class PyOCR(OCR):
    """OCR implementation using PyPDF and Tesseract."""

    def extract_text(self) -> Optional[str]:
        """Extract text using PyPDF and fallback to Tesseract if needed."""
        try:
            log.info(f"Extracting text from {self.pdf_path} using PyPDF.")
            with open(self.pdf_path, "rb") as file:
                reader = pypdf.PdfReader(file)
                text = "\n".join([page.extract_text() for page in reader.pages])
                if text.strip():
                    return text

            log.info("Text extraction failed. Falling back to Tesseract OCR.")
            images = convert_from_path(self.pdf_path)
            return "\n".join([pytesseract.image_to_string(img) for img in images])
        except Exception as e:
            log.debug(f"Error extracting text with PyPDF/Tesseract: {e}")
            return None


class OCRFactory:
    """Factory class to create OCR instances."""

    @staticmethod
    def create_ocr(ocr_type: OCRType, pdf_path: str) -> Optional[OCR]:
        """Create an OCR instance based on the type."""
        if ocr_type == OCRType.SURYA:
            return SuryaOCR(pdf_path)
        elif ocr_type == OCRType.PYPDF:
            return PyOCR(pdf_path)
        else:
            log.debug(f"Unsupported OCR type: {ocr_type}")
            return None