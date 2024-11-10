from datetime import datetime, timedelta, timezone
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import fahrenheit_to_celsius, inch_to_mm, initialize_driver, load_locations, mph_to_kmh

class TimeAndDateSpider(scrapy.Spider):
    name = "TimeAndDate"
    driver = None  # To store the WebDriver instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("TimeAndDate")
        self.driver = initialize_driver()

    def close(self, reason):
        if self.driver:
            self.driver.quit()

    def start_requests(self):
        for location in self.locations:
            yield SeleniumRequest(
                url=location.get('url'),
                callback=self.parse,
                wait_time=10,
                meta={
                    'city': location.get('city'),
                    'country': location.get('country'),
                    'state': location.get('state')
                }
            )

    def parse(self, response):
        self._accept_cookies()
        
        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state')
        current_date = datetime.now(timezone.utc)
        table_rows = response.css('#wt-ext > tbody > tr')
        
        for index, row in enumerate(table_rows):
            temp_text = row.css('td:nth-child(3)::text').get()
            temp_high, temp_low = self._extract_temperature(temp_text)
            
            weather_condition = row.css('td.small::text').get()
            wind_speed = self._extract_wind_speed(row)
            precipitation_chance = row.css('td:nth-child(9)::text').get()
            precipitation_amount = self._extract_precipitation_amount(row, index)
            humidity = self._extract_humidity(row, index)
            
            yield DayForecastItem(
                city=city,
                state=state,
                country=country,
                temp_high=temp_high,
                temp_low=temp_low,
                wind_speed=wind_speed,
                precipitation_chance=precipitation_chance.replace('%', ''),
                precipitation_amount=precipitation_amount,
                humidity=humidity,
                weather_condition=weather_condition,
                source="TimeAndDate",
                collection_date=current_date,
                forecasted_day=current_date + timedelta(days=index)
            )

    def _accept_cookies(self):
        try:
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'))
            )
            accept_button.click()
        except Exception as e:
            self.logger.info(f"Failed to find and click the accept button: {e}")

    # Helper Methods
    def _extract_temperature(self, temp_text):
        if temp_text:
            temps = temp_text.split('/')
            if '°F' in temp_text:
                return map(self.process_temperature, temps, ['F', 'F'])
            elif '°C' in temp_text:
                return map(self.process_temperature, temps, ['C', 'C'])
            return map(self.process_temperature, temps)
        return None, None

    def _extract_wind_speed(self, row):
        wind_speed_text = row.css('td:nth-child(6)::text').get()
        if wind_speed_text == 'N/A':
            return None
        if 'mph' in wind_speed_text:
            return mph_to_kmh(wind_speed_text.split()[0])
        return wind_speed_text.split()[0]

    def _extract_precipitation_amount(self, row, index):
        precipitation_amount = row.xpath(f'//*[@id="wt-ext"]/tbody/tr[{index + 1}]/td[9]/text()').get()
        if precipitation_amount == '-':
            return None
        precipitation_amount = precipitation_amount.replace(' mm', '').strip()
        if '°F' in row.css('td:nth-child(3)::text').get():
            precipitation_amount = inch_to_mm(float(precipitation_amount.replace('"', '').strip()))
        return precipitation_amount

    def _extract_humidity(self, row, index):
        humidity = row.xpath(f'//*[@id="wt-ext"]/tbody/tr[{index + 1}]/td[7]/text()').get()
        return humidity.replace('%', '').strip() if humidity else None

    def process_temperature(self, temp_text, unit=None):
        temp_text = temp_text.strip()
        if unit == 'F' or '°F' in temp_text:
            return fahrenheit_to_celsius(temp_text.replace('°F', '').strip())
        if unit == 'C' or '°C' in temp_text:
            return float(temp_text.replace('°C', '').strip())
        try:
            return float(temp_text)
        except ValueError:
            return None
