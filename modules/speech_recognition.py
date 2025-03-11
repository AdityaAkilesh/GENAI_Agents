import speech_recognition as sr

def transcribe_audio(audio_file):
    """Converts speech to text and returns structured output."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return {"transcription": text}
    except sr.UnknownValueError:
        return {"error": "Could not understand the audio."}
    except sr.RequestError:
        return {"error": "Speech recognition service is unavailable."}
