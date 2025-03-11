import google.generativeai as genai

def detect_spam(email_text):
    """Classifies an email as 'Spam' or 'Not Spam' and returns structured output."""
    if not email_text:
        return {"error": "No email content provided for spam detection."}
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Classify this email as 'Spam' or 'Not Spam': '{email_text}'")
    
    is_spam = "spam" in response.text.strip().lower()
    return {"email_content": email_text[:500], "classification": "Spam" if is_spam else "Not Spam"}
