import scrapy
from datetime import datetime
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
        state = response.meta.get('state')
        if state == '':
            state = None
        
        skip_first_five_counter = 0
        for day in response.css('summary.Disclosure--Summary--3GiL4'):
            skip_first_five_counter += 1
            if skip_first_five_counter <= 5:
                continue

            item = DayForecastItem()
            item['country'] = country
            item['state'] = state
            item['city'] = city
            item['date'] = datetime.now().strftime('%Y-%m-%d')
            item['day'] = day.css('h2.DetailsSummary--daypartName--kbngc::text').get()
            item['weather_condition'] = day.css('div.DetailsSummary--condition--2JmHb span::text').get()
            item['temp_high'] = day.css('span.DetailsSummary--highTempValue--3PjlX::text').get()
            item['temp_low'] = day.css('span.DetailsSummary--lowTempValue--2tesQ::text').get()
            item['precipitation'] = day.css('div.DetailsSummary--precip--1a98O span::text').get().replace('%', '')
            item['wind'] = day.css('span[data-testid="Wind"] span:nth-child(2)::text').extract_first()
            item['source'] = 'TheWeatherChannel'
            yield item
