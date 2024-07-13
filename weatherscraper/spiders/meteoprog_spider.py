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

class MeteoprogSpider(scrapy.Spider):
    name = "Meteoprog"
    locations = []  # Initialize locations as an empty list
    start_urls = [
        "https://www.meteoprog.com/review/Berlin/",
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
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]//div/div[2]/button[2]'))            )
            accept_button.click()
        except Exception as e:
            print(f"Failed to find and click the accept button: {e}")
            
            
        
        # Initialize variables to store data        
        city = ''
        h1_text = response.xpath('//h1/text()').get()
        if h1_text:
            city = h1_text.split()[-1]
            self.log(f"The last word is: {city}")
        
        # Initialize lists for collected data
        temp_high = []
        temp_low = []
        wind_speed = []
        precipitation = []

        # Extract temperature high
        temp_high_elements = response.css('text.column_textMax::text').getall()
        temp_high = [temp.strip() for temp in temp_high_elements]
        print(temp_high)

        # Extract temperature low
        temp_low_elements = response.css('text.column_textMin::text').getall()
        temp_low = [temp.strip() for temp in temp_low_elements]
        print(temp_low)


        # Extract wind speed
        for i in range(1, 15):
            wind_speed_selector = f'#weather-temp-graph-week > div > div > div.item-table > ul.wind-speed-list > li:nth-child({i}) > span::text'
            wind_speed.append(response.css(wind_speed_selector).get().strip())

        print(wind_speed)

        precipitation_elements = response.css('#weather-temp-graph-week > div > div > div.item-table > ul:nth-child(4) > li > span:first-child::text').getall()
        precipitation = [precip.strip() for precip in precipitation_elements]
        
        print(precipitation)

        # Create items from the collected data
        for i in range(14):
            item = DayForecastItem(
                country='', #I could save it in the locations link. I have specified locations anyway, there should be no confusion with country and state. I could even delete them.
                state='',
                city=city,
                weather_condition='',                
                temp_high=temp_high[i] if i < len(temp_high) else '',
                temp_low=temp_low[i] if i < len(temp_low) else '',
                precipitation=precipitation[i] if i < len(precipitation) else '',
                wind=wind_speed[i] if i < len(wind_speed) else '',
                source='MeteoProg'
            )
            yield item