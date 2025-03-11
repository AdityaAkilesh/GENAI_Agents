import google.generativeai as genai

def correct_grammar(text):
    """Corrects grammar and spelling of the given text, returning structured output."""
    if not text:
        return {"error": "No text provided for grammar correction."}
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Correct grammar: '{text}'")
    
    return {"original": text, "corrected": response.text.strip()}
