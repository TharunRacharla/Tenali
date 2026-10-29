import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

def listen():
    try:
        r = sr.Recognizer()
        mics = sr.Microphone.list_microphone_names()
        microphone_index = None

        for idx, name in enumerate(mics):
            if "microphone" in name.lower():
                microphone_index = idx
                logger.info(f"Using microphone: {name}")
                break

        try:
            if microphone_index is not None:
                source_mic = sr.Microphone(device_index=microphone_index)
            else:
                source_mic = sr.Microphone()

            with source_mic as source:
                r.adjust_for_ambient_noise(source, duration=1)
                logger.info("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)

        except OSError as e:
            logger.error(f"Microphone error: {e}")
            return "Microphone not found. Please check your audio input device."

        except sr.WaitTimeoutError:
            return "I didn't hear anything. Please try again."

        try:
            logger.info("Recognizing speech...")
            user_input = r.recognize_google(audio, language='en-in')
            logger.info(f"User said: {user_input}")
            return user_input

        except sr.UnknownValueError:
            return "Say that again please..."

        except sr.RequestError:
            return "Connection error - please check your internet."

    except Exception:
        logger.exception("Unexpected error in listen()")
        return "Something went wrong while listening."