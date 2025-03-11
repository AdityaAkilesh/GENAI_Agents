import google.generativeai as genai
import json
import re

def analyze_sentiment(text):
    """Analyzes sentiment and returns structured output."""
    if not text:
        return {"error": "No text provided for sentiment analysis."}
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"""
    Analyze the sentiment of the following text and return a structured JSON response.
    The response should contain:
    - `emotions`: A dictionary with emotion labels (Happy, Sad, Angry, Neutral) as keys and percentages as values.
    - `description`: A short sentiment summary.
    Return only JSON format.
    Text: '{text}'
    """)
    
    # Extract JSON from response
    try:
        sentiment_data = json.loads(response.text.strip())
        return sentiment_data
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response.", "raw_response": response.text.strip()}
