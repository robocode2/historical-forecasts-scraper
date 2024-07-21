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
        # Initialize variables to store data 
             
        city = ''
        h1_text = response.xpath('//h1/text()').get()
        if h1_text:
            city = h1_text.split()[-1]
            self.log(f"The last word is: {city}")
        
        # Initialize lists for collected data
        wind_speed = []
        precipitation = []



        # Extract wind speed
        for i in range(1, 15):
            wind_speed_selector = f'#weather-temp-graph-week > div > div > div.item-table > ul.wind-speed-list > li:nth-child({i}) > span::text'
            wind_speed.append(response.css(wind_speed_selector).get().strip())

        print(wind_speed)

        precipitation_elements = response.css('#weather-temp-graph-week > div > div > div.item-table > ul:nth-child(4) > li > span:first-child::text').getall()
        precipitation = [precip.strip() for precip in precipitation_elements]
        
        print(precipitation)
        
        forecast_days = response.xpath('//div[contains(@class, "swiper-slide")]')

        temp_max = []
        temp_min = []

        for day in forecast_days:
            max_temp = day.xpath('.//div[contains(@class, "temperature-max")]/h6/text()').get()
            min_temp = day.xpath('.//div[contains(@class, "temperature-min")]/h6/text()').get()

            temp_max.append(max_temp.strip().replace('°', '').replace('+', '').replace('C', '') if max_temp else '')
            temp_min.append(min_temp.strip().replace('°', '').replace('+', '').replace('C', '') if min_temp else '')

        print(temp_max, temp_max)

        # Create items from the collected data
        for i in range(14):
            item = DayForecastItem(
                country='Germany', #I could save it in the locations link. I have specified locations anyway, there should be no confusion with country and state. I could even delete them.
                state='Land Berlin',
                city=city,
                weather_condition='',                
                temp_high=temp_max[i].replace('°', '').replace('+', '') if i < len(temp_max) else '', #this is wrong
                temp_low=temp_min[i].replace('°', '').replace('+', '') if i < len(temp_min) else '',
                precipitation=precipitation[i] if i < len(precipitation) else '',
                wind=wind_speed[i] if i < len(wind_speed) else ''            )
            yield item