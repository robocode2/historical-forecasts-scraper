import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from weatherscraper.items import DayForecastItem
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class TimeAndDateSpider(scrapy.Spider):
    name = "TimeAndDate"
    start_urls = [
        "https://www.timeanddate.com/weather/germany/berlin/ext",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response):
        #driver = response.meta['driver']
          # Initialize Chrome driver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        # Handle cookies acceptance
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'))
            )
            accept_button.click()
        except Exception as e:
            self.logger.info(f"Failed to find and click the accept button: {e}")

        # Extract data from the table
        table_rows = response.css('#wt-ext > tbody > tr')

        for row in table_rows:
            # Extract temperatures
            temp_text = row.css('td:nth-child(3)::text').get()
            if temp_text:
                temp_high, temp_low = map(str.strip, temp_text.split('/'))
                temp_low = temp_low.replace('°C', '').strip()  # Remove °C from temp_low

            # Extract weather condition
            weather_condition = row.css('td.small::text').get()

            # Extract wind speed
            wind_speed_text = row.css('td:nth-child(6)::text').get()
            wind_speed = wind_speed_text.split()[0] if wind_speed_text else None  # Extract only the number

            # Extract precipitation
            precipitation = row.css('td:nth-child(9)::text').get()

            # Print extracted data for debugging
            print(f"High: {temp_high}, Low: {temp_low}, Condition: {weather_condition}, Wind: {wind_speed}, Precipitation: {precipitation}")

            # Create and yield the item
            item = DayForecastItem(
                city='Berlin',  # Manually set since we know the start URL is for Berlin
                state='Berlin',
                country='Germany',
                temp_high=temp_high,
                temp_low=temp_low,
                wind=wind_speed,
                precipitation=precipitation,
                weather_condition=weather_condition,
                source="TimeAndDate"
            )
            yield item