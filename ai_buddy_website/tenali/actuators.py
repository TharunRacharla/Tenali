import pyttsx3

def speak(audio):
    engine = pyttsx3.init('sapi5')  # Initialize a new engine instance each time
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180) 
    engine.say(audio)
    engine.runAndWait()
    engine.stop()  # Stop the engine to close the loop
    print(audio)