import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def load_locations(section_name):
    """
    Load locations from a JSON file based on the given section name.
    
    :param section_name: The section name to extract from the JSON file.
    :return: A list of locations if found, otherwise an empty list.
    """
    locations = []
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_file_path = os.path.join(current_dir, 'locations.json')
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            locations = data.get(section_name, [])
    except FileNotFoundError:
        print(f"locations.json file not found. Please make sure it exists and contains valid data.")
    except json.JSONDecodeError:
        print(f"Error decoding locations.json. Please ensure the JSON is valid.")
    
    return locations

def initializeDriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver