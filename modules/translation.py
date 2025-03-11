import google.generativeai as genai

def translate_text(text, target_language="fr"):
    """Translates text to the specified language and returns structured output."""
    if not text:
        return {"error": "No text provided for translation."}
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Translate this to {target_language}: '{text}'")
    
    return {"original": text, "translated": response.text.strip(), "language": target_language}
