import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser, wikipedia
import os, sys, random, pywhatkit as kit
import smtplib, pyjokes, requests
from bs4 import BeautifulSoup as bs
import cv2

# to send email
def sendEmail(to, content):
    """Sends an email to the specified recipient with the given content."""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('tharunracharla06442@gmail', 'your_password')
    server.sendmail('your_email', to, content)
    server.close()

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
        return "Say that again please..."
    return user_input

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
        
        search = "temperature in delhi"
        url = f"https://www.google.com/search?q={search}"
        r  = requests.get(url)
        data = bs(r.text,"html.parser")
        temp = data.find("div", class_ = "BNeawe").text
        speak(f"current{search} is {temp}")

    elif "send message" in user_input:
        speak("What should I say?")
        message = takeCommand().lower()
        kit.sendwhatmsg("+91---", message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
        speak("Message sent!")
        return "Message sent!"
    elif "no thanks" in user_input:
        speak("Thanks for using me. Have a nice day!")
        return 'exit'
    else:
        return f"Sorry, I didn't get that. Please try again. did you say {user_input}"
    

    speak("Sir, do you have any other work?")




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