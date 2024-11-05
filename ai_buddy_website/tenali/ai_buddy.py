import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser, wikipedia
import os, sys,  random, pywhatkit as kit
import smtplib
import cv2

# to send email
def sendEmail(to, content):
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

def process_input(user_input):
    if "open google" in user_input:
        speak("Sir, what should I search on Google?")
        search = takeCommand().lower()
        webbrowser.open(f"{search}")
        speak("Opening Google for you...")

    elif "open youtube" in user_input:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube...")
        return "Opening YouTube..."

    elif "play songs on youtube" in user_input:
        kit.playonyt("See you again")
        speak("playing songs on youtube")

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
        os.system(npath)
        speak("Opening Notepad...")
        return "Opening Notepad..."
    
    elif "open command prompt" in user_input:
        os.system("start cmd")
        speak("Opening Command Prompt...")
        return "Opening Command Prompt..."

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
        for song in songs:
            if song.endswith(".mp3"):
                os.startfile(os.path.join(music_dir, song))
                speak("Playing Music...")
        return "Playing Music..."

    elif "the time" in user_input:
        speak(f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}")
        return f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}"

    elif "the date" in user_input:
        speak(f"Current date is {datetime.datetime.now().strftime('%d/%m/%Y')}")
        return f"Current date is {datetime.datetime.now().strftime('%d/%m/%Y')}"

    elif "wikipedia" in user_input:
        speak("Searching Wikipedia...")
        user_input = user_input.replace("wikipedia", "")
        results = wikipedia.summary(user_input, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        return results
    
    elif "send message" in user_input:
        speak("What should I say?")
        message = takeCommand().lower()
        kit.sendwhatmsg("+91---", message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
        speak("Message sent!")
        return "Message sent!"
    
    elif "no thanks" in user_input:
        speak("Thanks for using me. Have a nice day!")
        sys.exit()

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