import scrapy
import re
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from weatherscraper.items import DayForecastItem

from weatherscraper.utils import load_locations, initializeDriver

class AccuWeatherSpider(scrapy.Spider):
    name = "AccuWeather"
    locations = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("AccuWeather")

    def start_requests(self):
        for location in self.locations:
            url = location.get('url')
            meta = {'city': location.get('city'), 'country': location.get('country'), 'state': location.get('state')}
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)

    def parse(self, response):
        driver = initializeDriver()

        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[1]/p'))
            )
            accept_button.click()
        except Exception as e:
            self.logger.warning(f"Failed to find and click the accept button: {e}")

        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state')
        if state == '':
           state = None
        
        daily_wrappers = response.css('div.page-column-1 div.daily-wrapper')[:14]

        for wrapper in daily_wrappers:
            temp_high = wrapper.css('a div.info span.high::text').get().strip().replace('°', '')
            temp_low = wrapper.css('a div.info span.low::text').get().strip().replace('°', '')
            temp_low = temp_low[1:]

            precip_div = wrapper.xpath('.//div[contains(@class, "precip")]')
            
            # Extract the text content after the SVG
            precipitation_percentage = precip_div.xpath('./text()[normalize-space()]').get().strip() if precip_div else None
            precipitation_percentage = precipitation_percentage.replace('%', '') if precipitation_percentage != None else None # TODOX tests due
            
            weather_condition = wrapper.css('div.phrase::text').get().strip()

            wind_text = wrapper.css('div.panels div.right p:nth-child(2) span.value::text').get()
            if wind_text:
                wind_speed_match = re.search(r'\b(\d+)\b', wind_text)
                wind_speed = int(wind_speed_match.group(1)) if wind_speed_match else None
            else:
                wind_speed = None
                
            item = DayForecastItem(
                city=city,
                state=state,
                country=country,
                temp_high=temp_high,
                temp_low=temp_low,
                precipitation=precipitation_percentage,
                weather_condition=weather_condition,
                wind=wind_speed,
                source='AccuWeather'
            )
            yield item