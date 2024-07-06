import json
import scrapy
from datetime import datetime
import time
import os
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from weatherscraper.items import DayForecastItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class AccuWeatherSpider(scrapy.Spider):
    name = "AccuWeather"
    locations = []  # Initialize locations as an empty list
    start_urls = [
        "https://www.accuweather.com/en/de/berlin/10178/daily-weather-forecast/178087",
       ]
        


    def start_requests(self):
          for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response):
        driver = response.meta['driver']
        """   # Initialize Chrome driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options) """
        
            
        try:
            # Attempt to find and click the accept cookies button
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]/p'))            )
            accept_button.click()
        except Exception as e:
            print(f"Failed to find and click the accept button: {e}")

        # Wait for the page to load the main content
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.page-column-1 div.daily-wrapper'))
        )
        
        # Extract city and state from header
        header_text = response.css('div.basic-header div.header-outer a.header-city-link h1::text').get()
        city, state = header_text.split(', ') if header_text else (None, None)
        
        
        daily_wrappers = response.css('div.page-column-1 div.daily-wrapper')

        for wrapper in daily_wrappers:
            # Extract temp_high and temp_low
            temp_high = wrapper.css('a div.info span.high::text').get().strip()
            temp_low = wrapper.css('a div.info span.low::text').get().strip()
            temp_low = temp_low[1:]
                
            # Extract precipitation
            precip_div = wrapper.css('div.precip')
            if precip_div:
                precipitation_percentage = precip_div.css('::text').get().strip()          
            print(precipitation_percentage)         
            # Extract weather condition
            weather_condition = wrapper.css('div.phrase::text').get().strip()
            

            # Create and yield the item
            item = DayForecastItem(
                city=city,
                state=state,
                country='',
                temp_high=temp_high,
                temp_low=temp_low,
                precipitation=precipitation_percentage,
                weather_condition=weather_condition,
                source='AccuWeather'
            )
            yield item