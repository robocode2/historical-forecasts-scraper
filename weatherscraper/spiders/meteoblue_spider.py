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

class MeteoblueSpider(scrapy.Spider):
    name = "Meteoblue"
    locations = []  # Initialize locations as an empty list
    start_urls = [
        "https://www.meteoblue.com/en/weather/14-days/berlin_germany_2950159",
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
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[10]/div[2]/div[1]/div[2]/div[2]/button[1]'))            )
            accept_button.click()
        except Exception as e:
            print(f"Failed to find and click the accept button: {e}")

        # Wait for the page to load the main content
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.forecast-table'))
        )
        
        rows = response.css('table.forecast-table tr')
        
        # Initialize variables to store data
        
        location_description = response.css('.location-description')
        country = location_description.css('.country a::text').get().strip()
        state = location_description.css('.admin a::text').get().strip()
        city = response.css('h1.main-heading::attr(content)').get()
        
        columns = [[] for _ in range(14)]

        # Iterate over the specified rows and collect data column-wise
        for row in rows[1:5] + rows[13:14]:  # rows 2-5 and row 14
            data = row.css('td::text').getall()
            if data:
                for i in range(14):
                    columns[i].append(data[i].strip() if i < len(data) else '')

        # Extract weather condition for each row
        weather_conditions = [[] for _ in range(14)]
        for row in rows:
            imgs = row.xpath('td/img')
            for i, img in enumerate(imgs):
                title = img.xpath('@title').get()
                weather_conditions[i].append(title.strip() if title else '')



        # Create items from the collected column-wise data
        for i in range(14):
            item = DayForecastItem(
                country=country,
                state=state,
                city=city,
                weather_condition=weather_conditions[i][0] if i < len(weather_conditions) else '',                
                temp_high=columns[i][2] if len(columns[i]) > 2 else '',
                temp_low=columns[i][3] if len(columns[i]) > 3 else '',
                precipitation=columns[i][4] if len(columns[i]) > 4 else '',
                wind='-',  # wind information is not available in the table,
                source='MeteoBlue'
            )
            yield item
