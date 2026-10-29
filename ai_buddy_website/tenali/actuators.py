import pyttsx3
import logging
import threading

logger = logging.getLogger(__name__)

# Initialize engine once at module level
_engine = None
_engine_lock = threading.Lock()

def _get_engine():
    """Get or create the TTS engine (singleton pattern)."""
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 180)
    return _engine

def speak(audio):
    """Convert text to speech and play audio output.
    
    Args:
        audio (str): Text content to be spoken
    
    Also prints the text to console for logging purposes.
    """
    try:
        with _engine_lock:
            engine = _get_engine()
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
            engine.say(audio)
            engine.runAndWait()
        logger.info(f"Speak: {audio}")
    except Exception as e:
        logger.error(f"TTS Error: {e}")
        print(f"Could not speak: {e}")