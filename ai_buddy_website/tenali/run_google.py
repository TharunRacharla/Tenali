from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager   
from .actuators import speak
from .sensors import listen
import time, os

# Check if ChromeDriver already exists
chromedriver_path = ChromeDriverManager().install()

# Check if the path exists, if not, download the driver
if not os.path.exists(chromedriver_path):
    print("ChromeDriver not found, downloading...")
    chromedriver_path = ChromeDriverManager().install()
else:
    print("ChromeDriver is already installed.")

def run_google(user_input):

    # Initialize the driver with the service
    service = Service(chromedriver_path)
    
    # Initialize the driver with the service
    driver = webdriver.Chrome(service=service)

    driver.maximize_window()

    # Ask for search query
    speak("Sir, what should I search on Google?")
    user_input = listen().lower()
    user_input = user_input.replace("AI Buddy", "").replace("google search", "").replace("google", "")

    speak("Searching Google...")
    driver.get("https://www.google.com")

    # Perform Google search
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(user_input)
    search_box.send_keys(Keys.RETURN)

    speak("Here are the search results.")
    time.sleep(2)

    # Define navigation commands
    while True:
        speak("Sir, what would you like to do? You can say back, forward, scroll, click a link, read content, or stop.")
        command = listen().lower()

        if "back" in command:
            driver.back()
            speak("Going back.")
        elif "forward" in command:
            driver.forward()
            speak("Going forward.")
        elif "scroll down" in command:
            driver.execute_script("window.scrollBy(0, 500);")
            speak("Scrolling down.")
        elif "scroll up" in command:
            driver.execute_script("window.scrollBy(0, -500);")
            speak("Scrolling up.")
        elif "click link" in command:
            speak("Please say the link text.")
            link_text = listen().lower()
            try:
                link = driver.find_element(By.PARTIAL_LINK_TEXT, link_text)
                link.click()
                speak(f"Clicking on the link {link_text}.")
            except:
                speak("Sorry, I couldn't find the link.")
        elif "read content" in command:
            try:
                content = driver.find_element(By.TAG_NAME, "body").text
                speak("This is the content of the page:")
                speak(content[:500])  # Reading first 500 characters for brevity
            except:
                speak("Unable to read the page content.")
        elif "stop" in command:
            speak("Closing Google.")
            driver.quit()
            break
        else:
            speak("Sorry, I didn't understand that command.")
