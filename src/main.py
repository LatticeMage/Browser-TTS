# main.py

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time
import configparser
from tts_jp import speak_text  # Import speak_text from tts_jp.py

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Get configurations from the INI file
try:
    gecko_driver_path = config.get('Settings', 'gecko_driver_path')
    kakuyomu_url = config.get('Settings', 'kakuyomu_url')
except configparser.Error as e:
    print(f"Error reading config.ini: {e}")
    exit()

# Set up the Firefox service with the path to geckodriver
service = Service(executable_path=gecko_driver_path)

# Create a new Firefox browser instance
driver = webdriver.Firefox(service=service)

try:
    # Open the Kakuyomu page
    driver.get(kakuyomu_url)
    time.sleep(3)  # Give the page time to fully load

    previous_selected_text = ""

    while True:  # Keep the loop running until manually stopped
        # Execute JavaScript to get the selected text
        selected_text = driver.execute_script(
            """
            var selection = window.getSelection();
            return selection.toString();
            """
        )

        if selected_text and selected_text != previous_selected_text:
             # Print the selected text if it's new
            print("Selected Text:", selected_text)
            speak_text(selected_text) # Trigger TTS
            previous_selected_text = selected_text
        elif not selected_text:
            if previous_selected_text != "":
                print("No text selected.")
                previous_selected_text = ""
            
        time.sleep(1) # Check every 1 second (adjust as needed)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()