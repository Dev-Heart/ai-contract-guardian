import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path: str):
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
    
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    
    return text.strip()

def save_text_for_debugging(text: str, filename: str = "extracted_text.txt"):
    """
    Saves extracted text to a file for manual verification.
    """
    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return output_path
