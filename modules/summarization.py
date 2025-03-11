import google.generativeai as genai

def summarize_text(text):
    """Summarizes the given text and ensures clean text output."""
    if not text:
        return "No text provided for summarization."
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"""
    Summarize the following text by extracting key insights while avoiding sensitive details like SSNs.
    Return only the summary text without JSON formatting.
    
    Text: '{text}'
    """)

    # Ensure the response contains valid text
    return response.text.strip() if response and hasattr(response, 'text') else "Failed to generate summary."