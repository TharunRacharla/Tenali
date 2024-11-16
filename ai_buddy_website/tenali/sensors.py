import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            # Attempt to listen with specified timeout and phrase time limit
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            # Handle the case where no audio input was detected within the timeout
            print("Listening timed out. No audio input detected.")
            return "Timeout"

    try:
        print("Recognizing...")
        user_input = r.recognize_google(audio, language='en-in')
        print(f"User said: {user_input}\n")

    except sr.UnknownValueError:
        # If speech was unintelligible
        return "Say that again please..."
    except sr.RequestError:
        # Handle API or network issues
        return "Connection error"

    return user_input