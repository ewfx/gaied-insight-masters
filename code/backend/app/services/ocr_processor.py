import pytesseract
import pdfplumber
from PIL import Image

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_image(image_path: str) -> str:
    """Extracts text from an image file using OCR."""
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)
