# main.py

import time
import configparser

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tts_jp import speak_text

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Get configurations from the INI file
try:
    gecko_driver_path = config.get('Settings', 'gecko_driver_path')
except configparser.Error as e:
    print(f"Error reading config.ini: {e}")
    exit()

# Set up the Firefox service with the path to geckodriver
service = Service(executable_path=gecko_driver_path)

# Create a new Firefox browser instance
driver = webdriver.Firefox(service=service)

# Load JavaScript code from file
try:
    with open('selection_script.js', 'r') as f:
        js_code = f.read()
except FileNotFoundError:
    print("Error: selection_script.js not found")
    exit()
except Exception as e:
    print(f"Error reading selection_script.js: {e}")
    exit()


try:
    # Open a default URL (optional)
    driver.get("about:blank")

    previous_spoken_text = ""
    while True:
        # Inject the JavaScript into the current tab
        driver.execute_script(js_code)

        # Wait for speakText to be set or changed
        try:
           WebDriverWait(driver, 10).until(lambda d: d.execute_script("return window.speakText != undefined;"))
        except Exception as e:
             print(f"Timeout or unexpected error while waiting for window.speakText: {e}")
             continue

        selected_text = driver.execute_script("return window.speakText;")

        if selected_text and selected_text != previous_spoken_text:
            print("Selected Text to Speak:", selected_text)
            speak_text(selected_text)
            previous_spoken_text = selected_text
            driver.execute_script("window.speakText = undefined;")  # reset after use
        elif not selected_text:
            previous_spoken_text = ""
             
        time.sleep(1)  # small delay to reduce resource usage

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()