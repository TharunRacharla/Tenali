import datetime, webbrowser, wikipedia
import os, random, pywhatkit as kit
import smtplib, pyjokes, requests, time
from bs4 import BeautifulSoup as bs
import cv2, subprocess
from .weather_bot import get_weather_info
from .actuators import speak
from .sensors import listen
from .run_google import run_google

# Global state to track if the assistant is active or asleep
active = True

def sendEmail(to, content):
    """Sends an email to the specified recipient with the given content."""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('tharunracharla06442@gmail', 'your_password')
    server.sendmail('your_email', to, content)
    server.close()

def process_input(user_input):
    global active

    # Wake Up Command
    if "wake up" in user_input:
        active = True
        speak("I am awake now. How can I assist you?")
        return "Awake"

    # Check if Assistant is Asleep
    if not active:
        speak("I am currently asleep. Say 'wake up' to activate me.")
        return "Asleep"

    # Sleep Command
    if "go to sleep" in user_input or "sleep now" in user_input:
        active = False
        speak("I am going to sleep now. Say 'wake up' to activate me.")
        return "Sleeping"

    # Remaining Commands (only processed when active)
    if "open google" in user_input:
        return run_google(user_input)
    elif "open youtube" in user_input:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube...")
        return "Opening YouTube..."
    elif "play songs on youtube" in user_input:
        speak("Sir, which song do you want to listen?")
        search = listen().lower()
        kit.playonyt(search)
        speak(f"Playing {search} on YouTube")
        return f"Playing {search} on YouTube"
    elif "send email to tharun" in user_input:
        try:
            speak("What should I say?")
            content = listen().lower()
            to = "tharunracharla06442@gmail.com"
            sendEmail(to, content)
            speak("Email has been sent to Tharun!")
        except Exception as e:
            print(e)
            speak("Sorry. I am not able to send this email to Tharun.")
        return "Email Sent"
    elif "play music" in user_input:
        music_dir = "C:\\Users\\HP\\Music\\Anime Bangers🍜_SpotifyDown_com"
        songs = os.listdir(music_dir)
        song = random.choice([s for s in songs if s.endswith(".mp3")])
        os.startfile(os.path.join(music_dir, song))
        speak("Playing music...")
        return "Playing Music"
    elif "the time" in user_input:
        time_str = datetime.datetime.now().strftime('%H:%M:%S')
        speak(f"Current time is {time_str}")
        return f"Current time is {time_str}"
    elif "the date" in user_input:
        date_str = datetime.datetime.now().strftime('%d/%m/%Y')
        speak(f"Current date is {date_str}")
        return f"Current date is {date_str}"
    elif "tell me a joke" in user_input:
        joke = pyjokes.get_joke()
        speak(joke)
        return joke
    elif "shut down the system" in user_input:
        speak("Shutting down the system...")
        os.system("shutdown /s /t 5")
        return "Shutting Down"
    elif "restart the system" in user_input:
        speak("Restarting the system...")
        os.system("shutdown /r /t 5")
        return "Restarting"
    elif "wikipedia" in user_input:
        speak("Searching Wikipedia...")
        user_input = user_input.replace("wikipedia", "")
        results = wikipedia.summary(user_input, sentences=5)
        speak("According to Wikipedia")
        speak(results)
        return results
    
    elif "weather" in user_input:
        speak("Fetching weather information...")
        info = get_weather_info(user_input)
        speak(info)
        return get_weather_info(user_input)
    
    # elif "no thanks" in user_input:
    #     speak("Thanks for using me. Have a nice day!")
    #     return "Exit"

    time.sleep(1)
    speak("Sir, do you have any other work?")
    return "Awaiting Command"
