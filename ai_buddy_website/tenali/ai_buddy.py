import datetime, webbrowser, wikipedia
import os, random, pywhatkit as kit
import smtplib, pyjokes, time, logging
from .weather_bot import get_weather_info
from .actuators import speak
from .sensors import listen
from .run_google import run_google
from .run_notepad import run_notepad
from .nlp_engine import parse_input

# Configure logging
logger = logging.getLogger(__name__)

# Global state to track if the assistant is active or asleep
active = True

def sendEmail(to, content):
    """Sends an email to the specified recipient with the given content.
    
    Args:
        to (str): Recipient email address
        content (str): Email content
    
    Returns:
        str: Status message ('EmailSent', 'EmailNotConfigured', or 'EmailFailed')
    """
    # Read email credentials from environment variables
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USER)
    if not EMAIL_USER or not EMAIL_PASS:
        msg = "Email credentials are not configured. Please set EMAIL_USER and EMAIL_PASS in .env."
        speak(msg)
        logger.warning(msg)
        return "EmailNotConfigured"
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, to, content)
        server.quit()
        logger.info(f"Email sent to {to}")
        return "EmailSent"
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        speak("Sorry. I am not able to send this email.")
        return "EmailFailed"

def process_input(user_input):
    """Process user input and execute corresponding AI buddy commands.
    
    Args:
        user_input (str): The user's voice input command
    
    Returns:
        str: Response message from AI buddy
    """
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

    # Use NLU to parse intent & entities
    parsed = parse_input(user_input)

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
            speak("Whom should I send this to? Can you please provide the email address?")
            to = listen().lower()
            sendEmail(to, content)
            speak("Email has been sent to Tharun!")
        except Exception as e:
            print(e)
            speak("Sorry. I am not able to send this email to Tharun.")
        return "Email Sent" 
    elif "play music" in user_input:
        try:
            music_dir = os.getenv("MUSIC_DIRECTORY", os.path.expanduser("~/Music"))
            if not os.path.exists(music_dir):
                speak(f"Music directory not found: {music_dir}")
                logger.warning(f"Music directory not found: {music_dir}")
                return "Music Directory Not Found"
            songs = os.listdir(music_dir)
            mp3_songs = [s for s in songs if s.endswith(".mp3")]
            if not mp3_songs:
                speak("No MP3 files found in music directory")
                return "No Music Files"
            song = random.choice(mp3_songs)
            os.startfile(os.path.join(music_dir, song))
            speak("Playing music...")
            logger.info(f"Playing song: {song}")
            return "Playing Music"
        except Exception as e:
            logger.error(f"Error playing music: {e}")
            speak("Sorry, I couldn't play music.")
            return "Music Error"
    elif "the time" in user_input:
        time_str = datetime.datetime.now().strftime('%H:%M:%S')
        speak(f"Current time is {time_str}")
        logger.info(f"Time requested: {time_str}")
        return f"Current time is {time_str}"
    elif "the date" in user_input:
        date_str = datetime.datetime.now().strftime('%d/%m/%Y')
        speak(f"Current date is {date_str}")
        logger.info(f"Date requested: {date_str}")
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
        try:
            speak("Searching Wikipedia...")
            search_query = user_input.replace("wikipedia", "").strip()
            results = wikipedia.summary(search_query, sentences=5)
            speak("According to Wikipedia")
            speak(results)
            logger.info(f"Wikipedia search: {search_query}")
            return results
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            speak("Sorry, I couldn't find information on Wikipedia.")
            return "Wikipedia Error"
    elif "write a note" in user_input:
        run_notepad()
    # Use NLU to parse intent & entities

    elif parsed.get('intent') == 'weather' or "weather" in user_input:
        city = parsed.get('entities', {}).get('city')
        speak("Fetching weather information...")
        if city:
            info = get_weather_info(f"weather in {city}")
        else:
            info = get_weather_info(user_input)
        speak(info)
        return info
    
    # elif "no thanks" in user_input:
    #     speak("Thanks for using me. Have a nice day!")
    #     return "Exit"

    time.sleep(1)
    speak("Sir, do you have any other work?")
    return "Awaiting Command"
