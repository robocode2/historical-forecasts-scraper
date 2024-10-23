import scrapy
from datetime import datetime, timedelta, timezone
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import load_locations

class TheWeatherChannelSpider(scrapy.Spider):
    name = "TheWeatherChannel"
    locations = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("TheWeatherChannel")

    def start_requests(self):
        for location in self.locations:
            url = location.get('url') + '?unit=m'
            meta = {'city': location.get('city'), 'country': location.get('country'), 'state': location.get('state')}
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)

    def parse(self, response):
        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state') or ''
        current_date = datetime.now(timezone.utc)
        

        for i in range(15):
            day_selector = f'//*[@id="detailIndex{i}"]'

            # Extract humidity
            humidity = response.xpath(day_selector + '/div/div[2]/ul/li[1]/div/span[2]/text()').get()
            if humidity:
                humidity = humidity.replace('%', '').strip()

            item = DayForecastItem()
            item['country'] = country
            item['state'] = state
            item['city'] = city
     

            if i == 0:
                item['precipitation_chance'] = response.xpath('//*[@id="detailIndex0"]/div/div[1]/div/div[3]/div[1]/span/text()').get()
                item['weather_condition'] = response.xpath('//*[@id="detailIndex0"]/div/div[1]/div/div[2]/svg/title/text()').get()
            else:
                item['precipitation_chance'] = (
                response.xpath(day_selector + '/div[@class="DailyContent--precipIconBlock--LoWxx"]/span[@class="DailyContent--value--Xgh8M"]/text()').get() or
                response.xpath(day_selector + '/summary/div/div/div[3]/span[@data-testid="PercentageValue"]/text()').get()
            )
                item['weather_condition'] = response.xpath(day_selector + '/div[@class="DetailsSummary--condition--2JmHb"]/span/text()').get() or \
                response.xpath(day_selector + '/summary/div/div/div[1]/svg/title/text()').get()

                
            if item['precipitation_chance']:
                item['precipitation_chance'] = item['precipitation_chance'].replace('%', '').strip()
            else:
                item['precipitation_chance'] = None
            
            item['precipitation_amount'] = None

            item['wind_speed'] = response.xpath(day_selector + '/div/div[1]/div/div[3]/div[2]/span/span[2]/text()').get() or \
                response.xpath(day_selector + '/div/div[1]/div/div[3]/div[2]/span/span[2]/text()').get()

            item['humidity'] = humidity
            item['source'] = 'TheWeatherChannel'
            
            temp_high = response.xpath(day_selector + '//*[contains(@class, "DetailsSummary--highTempValue")]/text()').get()
            item['temp_high'] = temp_high if temp_high != "--" else None

            temp_low = response.xpath(day_selector + '//*[contains(@class, "DetailsSummary--lowTempValue")]/text()').get()
            item['temp_low'] = temp_low if temp_low != "--" else None
            
            item['collection_date'] = current_date  
            item['forecasted_day'] = current_date + timedelta(days=i) 
            yield item