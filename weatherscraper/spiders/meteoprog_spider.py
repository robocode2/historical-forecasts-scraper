import scrapy
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import load_locations
  
class MeteoprogSpider(scrapy.Spider):
    name = "MeteoProg"
    locations = [] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("MeteoProg")

    def start_requests(self):
        for location in self.locations:
            url = location.get('url')
            meta = {'city': location.get('city'), 'country': location.get('country'), 'state': location.get('state')}
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)


    def parse(self, response):
        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state')
                     
        wind_speed = []
        precipitation = []

        for i in range(1, 15):
            wind_speed_selector = f'#weather-temp-graph-week > div > div > div.item-table > ul.wind-speed-list > li:nth-child({i}) > span::text'
            wind_speed.append(response.css(wind_speed_selector).get().strip())

        precipitation_elements = response.css('#weather-temp-graph-week > div > div > div.item-table > ul:nth-child(4) > li > span:first-child::text').getall()
        precipitation = [precip.strip() for precip in precipitation_elements]
                
                
        forecast_days = response.xpath('//div[contains(@class, "swiper-slide")]')
        temp_max = []
        temp_min = []

        for day in forecast_days:
            max_temp = day.xpath('.//div[contains(@class, "temperature-max")]/h6/text()').get()
            min_temp = day.xpath('.//div[contains(@class, "temperature-min")]/h6/text()').get()

            temp_max.append(max_temp.strip().replace('°', '').replace('+', '').replace('C', '') if max_temp else '')
            temp_min.append(min_temp.strip().replace('°', '').replace('+', '').replace('C', '') if min_temp else '')

        for i in range(14):
            item = DayForecastItem(
                country=country,
                state=state,
                city=city,
                weather_condition='',                
                temp_high=temp_max[i] if i < len(temp_max) else '', #this is wrong
                temp_low=temp_min[i] if i < len(temp_min) else '',
                precipitation=precipitation[i] if i < len(precipitation) else '',
                wind=wind_speed[i] if i < len(wind_speed) else '',
                source='MeteoProg')
            yield item