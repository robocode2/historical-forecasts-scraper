import scrapy
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WeatherSpider(scrapy.Spider):
    name = "weather"
    start_urls = [
        "https://weather.com/weather/tenday/l/153e65f344ab389e17703aae99cf18a182265e8095831d55ddfcfc6c5aa9a91c?unit=m"
    ]

    def start_requests(self):
        for url in self.start_urls:
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
        
        for day in response.css('summary.Disclosure--Summary--3GiL4'):
            item = DayForecastItem()
            item['day'] = day.css('h2.DetailsSummary--daypartName--kbngc::text').get()
            item['weather_condition'] = day.css('div.DetailsSummary--condition--2JmHb span::text').get()
            item['temp_high'] = day.css('span.DetailsSummary--highTempValue--3PjlX::text').get()
            item['temp_low'] = day.css('span.DetailsSummary--lowTempValue--2tesQ::text').get()
            item['precipitation'] = day.css('div.DetailsSummary--precip--1a98O span::text').get()
            item['wind'] = day.css('span[data-testid="Wind"] span:nth-child(2)::text').extract_first()

            yield item