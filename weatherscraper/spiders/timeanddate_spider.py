import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import initializeDriver, load_locations


class TimeAndDateSpider(scrapy.Spider):
    name = "TimeAndDate"
    locations = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("TimeAndDate")

    def start_requests(self):
        for location in self.locations:
            url = location.get('url')
            meta = {'city': location.get('city'), 'country': location.get('country'), 'state': location.get('state')}
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)

    def parse(self, response):
        driver = initializeDriver()
        
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'))
            )
            accept_button.click()
        except Exception as e:
            self.logger.info(f"Failed to find and click the accept button: {e}")


        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state')
        if state == '':
            state = None
            
            
        table_rows = response.css('#wt-ext > tbody > tr')

        for row in table_rows:
            temp_text = row.css('td:nth-child(3)::text').get()
            if temp_text:
                temp_high, temp_low = map(str.strip, temp_text.split('/'))
                temp_low = temp_low.replace('°C', '').strip() 

            weather_condition = row.css('td.small::text').get()

            wind_speed_text = row.css('td:nth-child(6)::text').get()
            wind_speed = wind_speed_text.split()[0] if wind_speed_text else None  # Extract only the number

            precipitation = row.css('td:nth-child(9)::text').get()


            item = DayForecastItem(
                city=city,
                state=state,
                country=country,
                temp_high=temp_high,
                temp_low=temp_low,
                wind=wind_speed,
                precipitation=precipitation,
                weather_condition=weather_condition,
                source="TimeAndDate"
            )
            yield item