import json
import scrapy
from datetime import datetime
import time
import os
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WeatherSpider(scrapy.Spider):
    name = "weather"
    locations = []  # Initialize locations as an empty list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items_seen = 0  # Counter for the items seen
         # Read the JSON file and load locations
        try:
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.realpath(__file__))
            json_file_path = os.path.join(current_dir, 'locations.json')

            with open(json_file_path, 'r') as file:
                self.locations = json.load(file)
        except FileNotFoundError:
            self.logger.error("locations.json file not found. Please make sure it exists and contains valid data.")

    def start_requests(self):
        # Iterate over each location
        for location in self.locations:
            url = location.get('url') 
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response):
        driver = response.request.meta['driver']
        
        # Switch to the cookie consent iframe and click the "Accept all" button
        try:
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe#sp_message_iframe_1100073'))
            )
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Accept all"]'))
            ).click()
            print("Successfully accepted cookies")
            # Allow time for the page to reload after accepting cookies
            time.sleep(3)
        except Exception as e:
            print("Could not accept cookies:", e)
        finally:
            driver.switch_to.default_content()

        # Ensure the page has reloaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'summary.Disclosure--Summary--3GiL4'))
        )
        
        # Scrape the location
        location = response.css('span.LocationPageTitle--PresentationName--1AMA6::text').get()
        city, state, country = None, None, None
        
        if location:
            location_parts = location.split(", ")
            if len(location_parts) == 3:
                city, state, country = location_parts
            elif len(location_parts) == 2:
                city, country = location_parts

        for day in response.css('summary.Disclosure--Summary--3GiL4'):
            self.items_seen += 1
            if self.items_seen <= 5:
                continue  # Skip the first 5 items

            item = DayForecastItem()
            item['country'] = country
            item['state'] = state
            item['city'] = city
            item['date'] = datetime.now().strftime('%Y-%m-%d')
            item['day'] = day.css('h2.DetailsSummary--daypartName--kbngc::text').get()
            item['weather_condition'] = day.css('div.DetailsSummary--condition--2JmHb span::text').get()
            item['temp_high'] = day.css('span.DetailsSummary--highTempValue--3PjlX::text').get()
            item['temp_low'] = day.css('span.DetailsSummary--lowTempValue--2tesQ::text').get()
            item['precipitation'] = day.css('div.DetailsSummary--precip--1a98O span::text').get()
            item['wind'] = day.css('span[data-testid="Wind"] span:nth-child(2)::text').extract_first()

            yield item