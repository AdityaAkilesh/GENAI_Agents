import google.generativeai as genai

def classify_text(text):
    """Classifies text into predefined categories and returns structured output."""
    if not text:
        return {"error": "No text provided for classification."}
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Classify this text and provide a confidence score: '{text}'")
    
    return {"original": text, "classification": response.text.strip()}
