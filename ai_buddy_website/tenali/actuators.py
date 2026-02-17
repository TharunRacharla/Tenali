import pyttsx3
import logging

logger = logging.getLogger(__name__)

def speak(audio):
    """Convert text to speech and play audio output.
    
    Args:
        audio (str): Text content to be spoken
    
    Also prints the text to console for logging purposes.
    """
    engine = pyttsx3.init('sapi5')  # Initialize a new engine instance each time
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180) 
    engine.say(audio)
    engine.runAndWait()
    engine.stop()  # Stop the engine to close the loop
    print(audio)