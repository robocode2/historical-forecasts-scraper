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
            print(url)
            meta = {'city': location.get('city'), 'country': location.get('country'), 'state': location.get('state')}
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)

    def parse(self, response):
        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state')
                     
        wind_speed = []
        humidity = []
        precipitation_amounts = []
        precipitation_chances = []
        weather_descriptions = []
        weather_elements = response.xpath('/html/body/div[4]/main/article/section[2]/div/div[3]/div/div/div[3]/div[2]')

        weather_descriptions = []
        for element in weather_elements:
            title = element.xpath('./@title').get()
            if title:
                weather_description = ', '.join(title.split(', ')[1:]) 
                weather_descriptions.append(weather_description)


        for i in range(1, 15):
            wind_speed_selector = f'#weather-temp-graph-week > div > div > div.item-table > ul.wind-speed-list > li:nth-child({i}) > span::text'
            wind_value = response.css(wind_speed_selector).get()
            wind_speed.append(wind_value.strip() if wind_value else None) 
        
        humidity_elements = response.xpath('//*[@id="weather-temp-graph-week"]/div/div/div[2]/ul[2]/li/span[1]/text()').getall()
        humidity = [h.strip().replace('%', '') for h in humidity_elements]


        precipitation_chance_elements = response.css('#weather-temp-graph-week > div > div > div.item-table > ul:nth-child(4) > li > span:first-child::text').getall()
        precipitation_chances = [precip.strip() for precip in precipitation_chance_elements]
        precipitation_chances.extend(["None"] * (14 - len(precipitation_chances)))

        precipitation_amount_elements = response.xpath('//*[@id="weather-temp-graph-week"]/div/div/div[2]/ul[5]/li/span[1]/text()').getall()
        precipitation_amounts = [p.strip().replace(' mm', '') for p in precipitation_amount_elements]


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
                temp_high=temp_max[i] if i < len(temp_max) else None, 
                temp_low=temp_min[i] if i < len(temp_min) else None,
                precipitation_chance=precipitation_chances[i], 
                precipitation_amount=precipitation_amounts[i] if i < len(precipitation_amounts) else None,
                humidity=humidity[i] if i < len(humidity) else None,
                wind_speed=float(wind_speed[i])*3.6 if i < len(wind_speed) and wind_speed[i] else None,
                weather_condition=weather_descriptions[i],
                source='MeteoProg'
            )
            yield item


