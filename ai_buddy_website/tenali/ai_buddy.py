import pyttsx3, speech_recognition as sr, datetime, webbrowser, wikipedia
import os, sys, random, pywhatkit as kit
import smtplib, pyjokes, requests, time
from bs4 import BeautifulSoup as bs
import cv2, spacy, subprocess
from .weather_bot import get_weather_info
from .actuators import speak
from .sensors import listen

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
    #run_google.py
    if "open google" in user_input:
        speak("Sir, what should I search on google?")
        user_input = listen().lower()
        import wikipedia as googleScrap
        user_input = user_input.replace("AI Buddy","")
        user_input = user_input.replace("google search","")
        user_input = user_input.replace("google","")
        speak("This is what I found on google")

        try:
            kit.search(user_input)
            result = googleScrap.summary(user_input, sentences=2)
            speak(result)

        except:
            speak("No speakable output available")
    #run_youtube.py
    elif "open youtube" in user_input:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube...")
        return "Opening YouTube..."
    #run_youtube.py
    elif "play songs on youtube" in user_input:
        speak("Sir, which song do you want to listen?")
        search = listen().lower()
        kit.playonyt(search)
        speak(f"playing {search} on youtube")
    #run_email.py
    elif "send email to tharun" in user_input:
        try:            
            speak("What should I say?")
            content = listen().lower()
            to = "tharunracharla06442@gmail.com"
            sendEmail(to, content)
            speak("Email has been sent to Tharun!")
        except Exception as e:
            print(e)
            speak("Sorry. I am not able to send this email to tharun...")
    #run_whatsapp.py
    elif "open whatsapp" in user_input:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp.... Scan the Code to Open your Whatsapp....")
        return "Opening WhatsApp..."
    #run_notepad.py
    elif "open notepad" in user_input:
        npath = "C:\\Windows\\system32\\notepad.exe"
        speak("Opening Notepad...")
        subprocess.Popen(npath)
        return "Opening Notepad..."
    #run_notepad.py
    elif "close notepad" in user_input:
        os.system("taskkill /f /im notepad.exe")
        speak("Closing Notepad...")
    #run_cmd.py
    elif "open command prompt" in user_input:
        speak("Opening Command Prompt...")
        subprocess.Popen("cmd.exe", shell=True)  # Opens Command Prompt without blocking
        return "Opening Command Prompt..."
    #run_cmd.py
    elif "close command prompt" in user_input:
        os.system("taskkill /f /im cmd.exe")
        speak("Closing Command Prompt...")
        return "Closing Command Prompt..."
    #run_camera.py
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
    #weather_bot.py
    elif "weather" in user_input:
        weather_info = get_weather_info(user_input)
        speak(weather_info)
    elif "send message" in user_input:
        speak("What should I say?")
        message = listen().lower()
        kit.sendwhatmsg("+91---", message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
        speak("Message sent!")
        return "Message sent!"
    elif "no thanks" in user_input:
        speak("Thanks for using me. Have a nice day!")
        return 'exit'   
    elif "wake up" in user_input:
        
        return "wake up buddy"

    time.sleep(1)
    speak("Sir, do you have any other work?")
    return "wake up buddy"