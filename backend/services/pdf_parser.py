import fitz  # PyMuPDF
import re
from typing import Tuple

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> Tuple[str, int]:
    """
    Extracts text from PDF byte content.
    Returns a tuple of (extracted_text, page_count).
    """
    if not pdf_bytes or len(pdf_bytes) == 0:
        raise ValueError("Uploaded PDF file is empty.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file. Ensure it is a valid PDF document. Error: {str(e)}")

    page_count = len(doc)
    extracted_text_list = []

    for page_num in range(page_count):
        page = doc[page_num]
        text = page.get_text("text")
        if text:
            extracted_text_list.append(text)

    doc.close()

    full_text = "\n".join(extracted_text_list)
    cleaned_text = clean_text(full_text)

    if not cleaned_text.strip():
        raise ValueError("Could not extract readable text from the PDF. It may be scanned or image-only.")

    return cleaned_text, page_count


def clean_text(text: str) -> str:
    """
    Normalizes whitespace, removes control characters, and cleans text.
    """
    if not text:
        return ""
    # Replace multiple newlines or tabs with single spaces/newlines
    text = re.sub(r'[\r\f\v]', ' ', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()
