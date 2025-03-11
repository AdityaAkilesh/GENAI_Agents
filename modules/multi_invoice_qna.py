import fitz  # PyMuPDF for PDF processing
import google.generativeai as genai
from modules.invoice_qna import answer_invoice_query
import io

def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    text = ""
    
    # Open PDF from BytesIO instead of a file path
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"

    return text.strip()

def process_multiple_invoices(pdf_files, query):
    """Processes multiple invoice PDFs and answers a specific query for each."""
    results = {}

    for i, pdf_file in enumerate(pdf_files, 1):
        pdf_file.seek(0)  # Reset file pointer before reading
        pdf_text = extract_text_from_pdf(pdf_file)

        if not pdf_text:
            results[f"Invoice {i}"] = {"error": "No text found in the PDF."}
        else:
            results[f"Invoice {i}"] = answer_invoice_query(pdf_text, query)

    return results
