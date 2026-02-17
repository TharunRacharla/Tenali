from .actuators import speak
from .sensors import listen
import time, os, pyautogui, subprocess

def run_notepad():
  speak("What should I write?")
  note_content = listen()  # Assuming listen() captures the user's voice input and converts it to text
  speak("Opening Notepad and writing your note.")

  # Open Notepad
  subprocess.Popen(['notepad.exe'])
  time.sleep(1)  # Wait for Notepad to open

  # Write the note
  pyautogui.typewrite(note_content)
  return "Note written"  # Return a message to indicate the action was completed