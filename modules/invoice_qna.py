import google.generativeai as genai
import json

def answer_invoice_query(invoice_text, query):
    """Processes an invoice and answers a specific query with structured JSON output."""
    if not invoice_text:
        return {"error": "No invoice content provided."}
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"""
    Based on this invoice: '{invoice_text}', answer: {query}
    Return the response as a structured JSON object without markdown formatting.
    """)
    
    # Ensure structured response by removing markdown artifacts
    raw_response = response.text.strip()

    try:
        json_response = json.loads(raw_response)
    except json.JSONDecodeError:
        json_response = {"answer": raw_response}  # Fallback if it's not proper JSON
    
    return json_response
