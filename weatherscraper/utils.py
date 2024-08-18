import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options

def load_locations(section_name):
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

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver


def save_response_html(self, response):
    os.makedirs('responses', exist_ok=True)
    file_path = 'responses/response.html'
    with open(file_path, 'wb') as f:
        f.write(response.body)

    self.log(f'Saved response HTML to {file_path}')