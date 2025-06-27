import google.generativeai as genai
from app.core.config import settings
from typing import Optional

_gemini_model: Optional[genai.GenerativeModel] = None

def init_gemini_model():
    global _gemini_model
    if _gemini_model is None:
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            _gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            print("Gemini 1.5 Flash model initialized successfully.")
        except Exception as e:
            print(f"ERROR: Failed to initialize Gemini model. Ensure GOOGLE_API_KEY is correct: {e}")
            _gemini_model = None

def get_gemini_model() -> genai.GenerativeModel:
    if _gemini_model is None:
        raise RuntimeError("Gemini model not initialized. Call init_gemini_model() on startup.")
    return _gemini_model