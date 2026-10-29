import datetime, webbrowser, wikipedia
import os, random, pywhatkit as kit
import smtplib, pyjokes, time, logging, re, subprocess, sys
from pathlib import Path
from .weather_bot import get_weather_info
from .actuators import speak
from .nlp_engine import parse_input
from .run_google import run_google

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
        logger.warning(msg)
        return "EmailNotConfigured"
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            refused_recipients = server.sendmail(EMAIL_FROM, to, content)
            if refused_recipients:
                logger.error("Email was refused for recipient(s): %s", refused_recipients)
                return "EmailFailed"
        logger.info(f"Email sent to {to}")
        return "EmailSent"
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return "EmailFailed"


def get_destructive_action(user_input):
    """Return a supported destructive action requested by the input, if any."""
    intent = parse_input(user_input).get("intent")
    if intent in {"shutdown", "restart"}:
        return intent
    return None


def execute_system_action(action):
    """Execute a destructive system action after the caller has confirmed it."""
    if action not in {"shutdown", "restart"}:
        raise ValueError(f"Unsupported system action: {action}")

    if sys.platform == "win32":
        command = ["shutdown", "/s" if action == "shutdown" else "/r", "/t", "5"]
    else:
        command = ["shutdown", "-h" if action == "shutdown" else "-r", "+0"]

    subprocess.run(command, check=True, timeout=10)
    return "Shutting down" if action == "shutdown" else "Restarting"

def process_input(user_input):
    """Process user input and execute corresponding AI buddy commands.
    
    Args:
        user_input (str): The user's voice input command
    
    Returns:
        str: Response message from AI buddy
    """
    global active
    user_input = user_input.strip().lower()

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
        search = user_input.partition("play songs on youtube")[2].strip()
        if not search:
            response = "Please enter a song after 'play songs on YouTube'."
            speak(response)
            return response
        kit.playonyt(search)
        speak(f"Playing {search} on YouTube")
        return f"Playing {search} on YouTube"
    elif parsed.get("intent") == "send_email":
        email_match = re.fullmatch(
            r"send email to ([^\s@]+@[^\s@]+) saying (.+)",
            user_input.strip(),
            re.IGNORECASE,
        )
        if not email_match:
            response = "To send an email, enter: send email to address@example.com saying your message."
            speak(response)
            return response

        status = sendEmail(email_match.group(1), email_match.group(2))
        responses = {
            "EmailSent": "Email sent successfully.",
            "EmailNotConfigured": "Email could not be sent because email credentials are not configured.",
            "EmailFailed": "Email could not be sent. Please check the recipient and email service settings.",
        }
        response = responses.get(
            status,
            "Email could not be sent because the email service returned an unknown status.",
        )
        speak(response)
        return response
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
            song_path = Path(music_dir, song).resolve()
            if not webbrowser.open(song_path.as_uri()):
                raise OSError(f"No application could open {song_path}")
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
    elif parsed.get("intent") in {"shutdown", "restart"}:
        action_name = "shut down" if parsed["intent"] == "shutdown" else "restart"
        response = f"Please confirm if you want to {action_name} this computer."
        speak(response)
        return response
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
        note_content = user_input.partition("write a note")[2].strip()
        if not note_content:
            response = "Please enter your note after 'write a note'."
            speak(response)
            return response
        response = f"Note: {note_content}"
        speak(response)
        return response
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
