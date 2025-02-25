# main.py

import time
import configparser

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

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

    while True:
        # Inject the JavaScript into the current tab
        driver.execute_script(js_code)
        time.sleep(1)  # small delay to reduce resource usage

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()