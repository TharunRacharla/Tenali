import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import smtplib

def speak(audio):
    engine = pyttsx3.init('sapi5')  # Initialize a new engine instance each time
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()
    engine.stop()  # Stop the engine to close the loop
    print(audio)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        return "Say that again please..."
    return query

#to make wish
import datetime


def process_input(user_input):
    if "open google" in user_input:
        webbrowser.open("https://www.google.com")
        speak("Opening Google...")
        return "Opening Google..."
    elif "open youtube" in user_input:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube...")
        return "Opening YouTube..."
    elif "open facebook" in user_input:
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook...")
        return "Opening Facebook..."
    elif "open instagram" in user_input:
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram...")
        return "Opening Instagram..."
    elif "open whatsapp" in user_input:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp.... Scan the Code to Open your Whatsapp....")
        return "Opening WhatsApp..."
    elif "open notepad" in user_input:
        npath = "C:\\Windows\\system32\\notepad.exe"
        os.system(npath)
        speak("Opening Notepad...")
        return "Opening Notepad..."
    else:
        return f"Sorry, I didn't get that. Please try again. did you say {user_input}"



# def wishMeDecorator(func):
#     def wrapper(*args, **kwargs):
#         # Get the current hour
#         hour = int(datetime.datetime.now().hour)

#         # Determine greeting based on the time of day
#         if 0 <= hour < 12:
#             speak("Good Morning!")
#         elif 12 <= hour < 18:
#             speak("Good Afternoon!")
#         else:
#             speak("Good Evening!")
        
#         # Personalized message
#         speak("I am AI Buddy. How may I help you?")
        
#         # Call the original function
#         return func(*args, **kwargs)
#     return wrapper