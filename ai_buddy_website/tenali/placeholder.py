import pyttsx3, speech_recognition as sr, datetime, webbrowser, wikipedia
import os, sys, random, pywhatkit as kit
import smtplib, pyjokes, requests, time
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import datetime, cv2, spacy
from bs4 import BeautifulSoup as bs
from .weather_bot import get_weather_info


class AIBuddy:
    def __init__(self):
        self.sleep_mode = False
        self.engine = pyttsx3.init()  # Initialize the engine once
        self.engine.setProperty('rate', 180)  # Set speaking rate
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Set voice preference
    
    def speak(self, text):
        """Converts text to speech only if not in sleep mode."""
        if not self.sleep_mode:
            print(text)
            self.engine.say(text)
            self.engine.runAndWait()

    def wake_up(self):
        """Wake up the AI Buddy."""
        self.sleep_mode = False
        response = "Hello again! What can I do for you?"
        self.speak(response)
        return response

    def sleep(self):
        """Put the AI Buddy to sleep."""
        self.sleep_mode = True
        response = "Going to sleep. Wake me up if you need anything!"
        self.speak(response)
        return response

    def wish_me(self):
        """Generate greeting based on the time of day."""
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good Morning!"
        elif hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        
        greeting += " I am AI Buddy. How may I help you?"
        self.speak(greeting)
        return greeting
    
    def sendEmail(self, to, content):
        """Sends an email to the specified recipient with the given content."""
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('tharunracharla06442@gmail', 'your_password')
        server.sendmail('your_email', to, content)
        server.close()
    
    def handle_user_input(self, user_input):
        """Process the user's input and return a response."""
        if self.sleep_mode and user_input != "wake up buddy":
            return "I'm currently asleep. Say 'wake up buddy' to activate me."

        if user_input == "wake up buddy":
            return self.wake_up()
        elif user_input == "sleep":
            return self.sleep()
        
        elif "open google" in user_input:
            self.speak("Sir, what should I search on google?")
            user_input = self.takeCommand().lower()
            import wikipedia as googleScrap
            user_input = user_input.replace("Tenali","")
            user_input = user_input.replace("google search","")
            user_input = user_input.replace("google","")
            self.speak("This is what I found on google")

            try:
                kit.search(user_input)
                result = googleScrap.summary(user_input, sentences=2)
                self.speak(result)

            except:
                self.speak("No speakable output available")

        elif "open youtube" in user_input:
            webbrowser.open("https://www.youtube.com")
            self.speak("Opening YouTube...")
            return "Opening YouTube..."

        elif "play songs on youtube" in user_input:
            self.speak("Sir, which song do you want to listen?")
            search = self.takeCommand().lower()
            kit.playonyt(search)
            self.speak(f"playing {search} on youtube")

        elif "send email to tharun" in user_input:
            try:            
                self.speak("What should I say?")
                content = self.takeCommand().lower()
                to = "tharunracharla06442@gmail.com"
                self.sendEmail(to, content)
                self.speak("Email has been sent to Tharun!")
            except Exception as e:
                print(e)
                self.speak("Sorry. I am not able to send this email to tharun...")

        elif "open whatsapp" in user_input:
            webbrowser.open("https://web.whatsapp.com")
            self.speak("Opening WhatsApp.... Scan the Code to Open your Whatsapp....")
            return "Opening WhatsApp..."
        
        elif "open notepad" in user_input:
            npath = "C:\\Windows\\system32\\notepad.exe"
            self.speak("Opening Notepad...")
            os.system(npath)
            return "Opening Notepad..."
        
        elif "close notepad" in user_input:
            os.system("taskkill /f /im notepad.exe")
            self.speak("Closing Notepad...")
        
        elif "open command prompt" in user_input:
            os.system("start cmd")
            self.speak("Opening Command Prompt...")
            return "Opening Command Prompt..."

        elif "close command prompt" in user_input:
            os.system("taskkill /f /im cmd.exe")
            self.speak("Closing Command Prompt...")
            return "Closing Command Prompt..."

        elif "open camera" in user_input:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(58)
                if k == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in user_input:
            music_dir = "C:\\Users\\HP\\Music\\Anime Bangers🍜_SpotifyDown_com"
            songs = os.listdir(music_dir)
            if songs.endswith(".mp3"):
                os.startfile(os.path.join(music_dir, random.choice(songs)))
                self.speak("Playing Music...")
            return "Playing Music..."

        elif "the time" in user_input:
            self.speak(f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}")
            return f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}"

        elif "the date" in user_input:
            self.speak(f"Current date is {datetime.datetime.now().strftime('%d/%m/%Y')}")
            return f"Current date is {datetime.datetime.now().strftime('%d/%m/%Y')}"

        elif "tell me a joke" in user_input:
            self.speak(pyjokes.get_joke())
            return pyjokes.get_joke()

        elif "shut down the system" in user_input:
            self.speak("Shutting down the system...")
            os.system("shutdown /s /t 5")
            return "Shutting down the system..."
        
        elif "restart the system" in user_input:
            self.speak("Restarting the system...")
            os.system("shutdown /r /t 5")
            return "Restarting the system..."
        elif "sleep the system" in user_input:
            self.speak("Sleeping the system...")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "Sleeping the system..."
        #to set alarm
        elif "set alarm" in user_input:
            nn = int(datetime.datetime.now().hour)
            if nn == 22:
                music_dir = "C:\\Users\\HP\\Music\\Anime Bangers🍜_SpotifyDown_com"
                songs = os.listdir(music_dir)
                if songs.endswith(".mp3"):
                    os.startfile(os.path.join(music_dir, songs[0]))
        elif "wikipedia" in user_input:
            self.speak("Searching Wikipedia...")
            user_input = user_input.replace("wikipedia", "")
            results = wikipedia.summary(user_input, sentences=5)
            print(results)
            self.speak("According to Wikipedia")
            self.speak(results)        

            return "thank you"

        elif "temperature" in user_input:
            search = "temperature in delhi"
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = bs(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            self.speak(f"current{search} is {temp}")
        
        elif "weather" in user_input:
            weather_info = get_weather_info(user_input)
            self.speak(weather_info)

        elif "send message" in user_input:
            self.speak("What should I say?")
            message = self.takeCommand().lower()
            kit.sendwhatmsg("+91---", message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
            self.speak("Message sent!")
            return "Message sent!"
        

        # Default response
        self.self.speak("I'm here to assist with your requests.")
        return "I'm here to assist with your requests."

# Initialize the AI Buddy instance
ai_buddy = AIBuddy()

@require_http_methods(["GET"])
def wish_me(request):
    """Initial greeting based on the time of day."""
    greeting = ai_buddy.wish_me()
    return JsonResponse({"greeting": greeting})

@require_http_methods(["POST"])
def handle_conversation(request):
    """Handles user commands, managing sleep/wake state."""
    user_input = request.POST.get("user_input", "").strip().lower()
    response = ai_buddy.handle_user_input(user_input)
    return JsonResponse({"user_input": user_input, "response": response, "sleep_mode": ai_buddy.sleep_mode})

def home(request):
    """Render the main chat page."""
    return render(request, "tenali/home.html")



# ========================================================================================\
# ========================================================================================

import pyttsx3, speech_recognition as sr, datetime, webbrowser, wikipedia
import os, sys, random, pywhatkit as kit
import smtplib, pyjokes, requests, time
from bs4 import BeautifulSoup as bs
import cv2, spacy
from .weather_bot import get_weather_info

def speak(audio):
    engine = pyttsx3.init('sapi5')  # Initialize a new engine instance each time
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180) 
    engine.say(audio)
    engine.runAndWait()
    engine.stop()  # Stop the engine to close the loop
    print(audio)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=10)

    try:
        print("Recognizing...")
        user_input = r.recognize_google(audio, language='en-in')
        print(f"User said: {user_input}\n")

    except Exception as e:
        speak("Sorry, I couldn't understand what you said. Please try again.")
        return "Say that again please..."
    return user_input

# to send email
def sendEmail(to, content):
    """Sends an email to the specified recipient with the given content."""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('tharunracharla06442@gmail', 'your_password')
    server.sendmail('your_email', to, content)
    server.close()

def process_input(user_input):
    if "open google" in user_input:
        speak("Sir, what should I search on google?")
        user_input = takeCommand().lower()
        import wikipedia as googleScrap
        user_input = user_input.replace("Tenali","")
        user_input = user_input.replace("google search","")
        user_input = user_input.replace("google","")
        speak("This is what I found on google")

        try:
            kit.search(user_input)
            result = googleScrap.summary(user_input, sentences=2)
            speak(result)

        except:
            speak("No speakable output available")

    elif "open youtube" in user_input:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube...")
        return "Opening YouTube..."

    elif "play songs on youtube" in user_input:
        speak("Sir, which song do you want to listen?")
        search = takeCommand().lower()
        kit.playonyt(search)
        speak(f"playing {search} on youtube")

    elif "send email to tharun" in user_input:
        try:            
            speak("What should I say?")
            content = takeCommand().lower()
            to = "tharunracharla06442@gmail.com"
            sendEmail(to, content)
            speak("Email has been sent to Tharun!")
        except Exception as e:
            print(e)
            speak("Sorry. I am not able to send this email to tharun...")

    elif "open whatsapp" in user_input:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp.... Scan the Code to Open your Whatsapp....")
        return "Opening WhatsApp..."
    
    elif "open notepad" in user_input:
        npath = "C:\\Windows\\system32\\notepad.exe"
        speak("Opening Notepad...")
        os.system(npath)
        return "Opening Notepad..."
    
    elif "close notepad" in user_input:
        os.system("taskkill /f /im notepad.exe")
        speak("Closing Notepad...")
    
    elif "open command prompt" in user_input:
        os.system("start cmd")
        speak("Opening Command Prompt...")
        return "Opening Command Prompt..."

    elif "close command prompt" in user_input:
        os.system("taskkill /f /im cmd.exe")
        speak("Closing Command Prompt...")
        return "Closing Command Prompt..."

    elif "open camera" in user_input:
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('webcam', img)
            k = cv2.waitKey(58)
            if k == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    elif "play music" in user_input:
        music_dir = "C:\\Users\\HP\\Music\\Anime Bangers🍜_SpotifyDown_com"
        songs = os.listdir(music_dir)
        if songs.endswith(".mp3"):
            os.startfile(os.path.join(music_dir, random.choice(songs)))
            speak("Playing Music...")
        return "Playing Music..."

    elif "the time" in user_input:
        speak(f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}")
        return f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}"

    elif "the date" in user_input:
        speak(f"Current date is {datetime.datetime.now().strftime('%d/%m/%Y')}")
        return f"Current date is {datetime.datetime.now().strftime('%d/%m/%Y')}"

    elif "tell me a joke" in user_input:
        speak(pyjokes.get_joke())
        return pyjokes.get_joke()

    elif "shut down the system" in user_input:
        speak("Shutting down the system...")
        os.system("shutdown /s /t 5")
        return "Shutting down the system..."
    
    elif "restart the system" in user_input:
        speak("Restarting the system...")
        os.system("shutdown /r /t 5")
        return "Restarting the system..."
    elif "sleep the system" in user_input:
        speak("Sleeping the system...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Sleeping the system..."
    #to set alarm
    elif "set alarm" in user_input:
        nn = int(datetime.datetime.now().hour)
        if nn == 22:
            music_dir = "C:\\Users\\HP\\Music\\Anime Bangers🍜_SpotifyDown_com"
            songs = os.listdir(music_dir)
            if songs.endswith(".mp3"):
                os.startfile(os.path.join(music_dir, songs[0]))
    elif "wikipedia" in user_input:
        speak("Searching Wikipedia...")
        user_input = user_input.replace("wikipedia", "")
        results = wikipedia.summary(user_input, sentences=5)
        print(results)
        speak("According to Wikipedia")
        speak(results)        

        return "thank you"

    elif "temperature" in user_input:
        search = "temperature in delhi"
        url = f"https://www.google.com/search?q={search}"
        r  = requests.get(url)
        data = bs(r.text,"html.parser")
        temp = data.find("div", class_ = "BNeawe").text
        speak(f"current{search} is {temp}")
    
    elif "weather" in user_input:
        weather_info = get_weather_info(user_input)
        speak(weather_info)

    elif "send message" in user_input:
        speak("What should I say?")
        message = takeCommand().lower()
        kit.sendwhatmsg("+91---", message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
        speak("Message sent!")
        return "Message sent!"
    
    elif "no thanks" in user_input:
        speak("Thanks for using me. Have a nice day!")
        return 'exit'   
    elif "wake up" in user_input:
        return "wake up buddy"

    time.sleep(2)
    speak("Sir, do you have any other work?")
    return "wake up buddy"




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

















# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 11/12/24
import pyttsx3, speech_recognition as sr, datetime, webbrowser, wikipedia
import os, sys, random, pywhatkit as kit
import smtplib, pyjokes, requests, time
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import datetime, cv2, spacy
from bs4 import BeautifulSoup as bs
from .weather_bot import get_weather_info


class AIBuddy:
    def __init__(self):
        self.sleep_mode = False
        self.engine = pyttsx3.init('sapi5')  # Initialize the engine once
        self.engine.setProperty('rate', 180)  # Set speaking rate
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Set voice preference
        self.awaiting_search = False  # Track if the bot is waiting for a search term
        self.awaiting_alarm = False  # Track if the bot is awaiting alarm time

    def speak(self, text):
        """Converts text to speech only if not in sleep mode."""
        if not self.sleep_mode:
            try:
                # Stop any ongoing speech before starting a new one
                if self.engine._inLoop:
                    self.engine.endLoop()
                
                print(text)
                self.engine.say(text)
                self.engine.runAndWait()
            
            except RuntimeError as e:
                print(f"Error in speak function: {e}")

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("Timeout, no speech detected.")
                return "Say that again please..."
        try:
            print("Recognizing...")
            user_input = r.recognize_google(audio, language='en-in')
            print(f"User said: {user_input}\n")
            return user_input.lower()  # Convert to lowercase for easier command matching
        except sr.UnknownValueError:
            self.speak("Sorry, I couldn't understand what you said. Please try again.")
            return "Say that again please..."
        except sr.RequestError:
            self.speak("Sorry, I'm having trouble accessing the speech recognition service.")
            return "Please check your connection."

    def wake_up(self):
        """Wake up the AI Buddy."""
        self.sleep_mode = False
        response = "Hello again! What can I do for you?"
        self.speak(response)
        return response

    def wish_me(self):
        """Generate greeting based on the time of day."""
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good Morning!"
        elif hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        
        greeting += " I am AI Buddy. How may I help you?"
        self.speak(greeting)
        return greeting
    
    def sendEmail(self, to, content):
        """Sends an email to the specified recipient with the given content."""
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.sendmail('your_email', to, content)
        server.close()

    def set_alarm(self, alarm_time):
        """Sets an alarm at the specified time."""
        current_time = datetime.datetime.now()
        alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M")
        time_diff = alarm_time - current_time
        if time_diff.total_seconds() > 0:
            self.speak(f"Alarm set for {alarm_time.strftime('%H:%M')}")
            time.sleep(time_diff.total_seconds())
            self.speak("Alarm ringing!")
            # You can play music or sound here as an alarm
            self.play_music()

    def handle_user_input(self, user_input):
        """Process the user's input and return a response."""
        if self.sleep_mode and user_input != "wake up buddy":
            return "I'm currently asleep. Say 'wake up buddy' to activate me."

        if user_input == "wake up buddy":
            return self.wake_up()
        elif user_input == "sleep":
            self.sleep_mode = True
            self.speak("Going to sleep. Say 'wake up buddy' to activate me.")
            return "Going to sleep."

        if "set alarm" in user_input:
            self.speak("Please specify the time for the alarm in HH:MM format.")
            alarm_time = self.takeCommand()
            if self.is_valid_time(alarm_time):
                self.set_alarm(alarm_time)
            else:
                self.speak("Sorry, I couldn't understand the time. Please try again.")
            return "Setting alarm..."

        elif "open google" in user_input:
            self.speak("Sir, what should I search on google?")
            self.awaiting_search = True  # Set the state to wait for the search input
            return "Awaiting search term."

        elif "open youtube" in user_input:
            webbrowser.open("https://www.youtube.com")
            self.speak("Opening YouTube...")
            return "Opening YouTube..."

        elif "play music" in user_input:
            music_dir = "path_to_your_music_directory"
            songs = os.listdir(music_dir)
            if songs:
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir, song))
                self.speak("Playing music...")
            return "Playing music..."

        elif "send email" in user_input:
            try:
                self.speak("What should I say?")
                content = self.takeCommand()
                to = "recipient_email@example.com"
                self.sendEmail(to, content)
                self.speak("Email has been sent!")
            except Exception as e:
                print(e)
                self.speak("Sorry. I am not able to send the email.")

        elif "weather" in user_input:
            # If the user asks for weather, proceed directly
            weather_info = get_weather_info(user_input)
            self.speak(weather_info)
            return weather_info
        
        elif "wikipedia" in user_input:
            # If the user asks for Wikipedia info, proceed directly
            user_input = user_input.replace("wikipedia", "").strip()
            summary = wikipedia.summary(user_input, sentences=2)
            self.speak(summary)
            return summary
        
        # Handle the "awaiting_search" flag if a search is in progress
        elif self.awaiting_search:
            # If awaiting a search term, perform the search and reset the state
            user_input = user_input.replace("tenali", "")
            self.speak("This is what I found on Google")
            try:
                kit.search(user_input)
                result = wikipedia.summary(user_input, sentences=2)
                self.speak(result)
            except Exception as e:
                self.speak("No speakable output available")
            self.awaiting_search = False  # Reset search state after handling
            return f"Search result for {user_input}"

        else:
            self.speak("Sorry, I couldn't understand your request.")
        
        return "Request processed."

    def is_valid_time(self, time_str):
        """Checks if the time is in HH:MM format."""
        try:
            datetime.datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
