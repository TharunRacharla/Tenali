import re
from pathlib import Path
import spacy
import logging

logger = logging.getLogger(__name__)

# Attempt to load a trained spaCy NLU model (optional)
MODEL_PATH = Path(__file__).resolve().parent / 'ml_models' / 'nlu_model'
try:
    if MODEL_PATH.exists():
        NLU_NLP = spacy.load(str(MODEL_PATH))
    else:
        NLU_NLP = None
except Exception:
    NLU_NLP = None


def _predict_intent_with_model(text: str):
    """Predict intent using trained spaCy NLU model.
    
    Args:
        text (str): Input text to classify
    
    Returns:
        tuple: (intent_name, confidence_score) or (None, 0.0) if model unavailable
    """
    if not NLU_NLP:
        return None, 0.0
    doc = NLU_NLP(text)
    if not doc.cats:
        return None, 0.0
    # pick the intent with highest score
    intent, score = max(doc.cats.items(), key=lambda x: x[1])
    return intent, score


def _normalize_intent(intent_name: str) -> str:
    """Normalize label names from Intent.json to simplified internal intents."""
    name = (intent_name or '').lower()
    # Basic normalizations
    name = name.replace('query', '')
    name = name.replace(' ', '_')
    # Examples: "timequery" -> "time" if it contains 'time'
    if 'time' in name:
        return 'time'
    if 'weather' in name:
        return 'weather'
    if 'wikipedia' in name:
        return 'wikipedia'
    if 'greeting' in name:
        return 'greeting'
    if 'joke' in name:
        return 'joke'
    if 'shutdown' in name or 'shut' in name:
        return 'shutdown'
    if 'restart' in name:
        return 'restart'
    if 'email' in name:
        return 'send_email'
    # fallback to cleaned name
    return name


def parse_input(text: str) -> dict:
    """Parse user input to extract intent and entities.
    
    Uses hybrid approach:
    1. Attempts ML-based prediction with spaCy model (if available)
    2. Falls back to rule-based pattern matching
    
    Args:
        text (str): User input text
    
    Returns:
        dict: {"intent": str, "entities": dict}
            - intent: Detected command/intent name
            - entities: Extracted information (e.g., city for weather queries)
    """
    text = (text or '').strip()

    # Attempt ML prediction first
    intent, score = _predict_intent_with_model(text)
    if intent and score >= 0.6:
        normalized = _normalize_intent(intent)
        entities = {}
        # simple entity extraction for weather
        if normalized == 'weather':
            m = re.search(r'in\s+(.+)$', text, re.IGNORECASE)
            if m:
                entities['city'] = m.group(1).strip()
        return {'intent': normalized, 'entities': entities}

    # Fallback to rule-based rules below
    lower_text = text.lower()

    if any(k in lower_text for k in ["wake up", "wake"]):
        return {"intent": "wake_up", "entities": {}}
    if any(k in lower_text for k in ["go to sleep", "sleep now", "sleep"]):
        return {"intent": "sleep", "entities": {}}
    if "weather" in lower_text:
        # attempt to extract city after the word 'in'
        m = re.search(r"in\s+(.+)$", lower_text)
        entities = {}
        if m:
            entities['city'] = m.group(1).strip()
        return {"intent": "weather", "entities": entities}
    if "wikipedia" in lower_text:
        return {"intent": "wikipedia", "entities": {}}
    if any(k in lower_text for k in ["open google", "google search", "google"]):
        return {"intent": "open_google", "entities": {}}
    if any(k in lower_text for k in ["open youtube", "youtube"]):
        return {"intent": "open_youtube", "entities": {}}
    if any(k in lower_text for k in ["play songs on youtube", "play song", "play music", "play"]):
        return {"intent": "play_music", "entities": {}}
    if any(k in lower_text for k in ["send email", "email"]):
        return {"intent": "send_email", "entities": {}}
    if "time" in lower_text:
        return {"intent": "time", "entities": {}}
    if "date" in lower_text:
        return {"intent": "date", "entities": {}}
    if "joke" in lower_text:
        return {"intent": "joke", "entities": {}}
    if any(k in lower_text for k in ["shutdown", "shut down", "shut the system"]):
        return {"intent": "shutdown", "entities": {}}
    if any(k in lower_text for k in ["restart the system", "restart"]):
        return {"intent": "restart", "entities": {}}

    # fallback
    return {"intent": "unknown", "entities": {}}