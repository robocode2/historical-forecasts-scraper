import scrapy
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import load_locations

class MeteoblueSpider(scrapy.Spider):
    name = "MeteoBlue"
    locations = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("MeteoBlue")

    def start_requests(self):
        for location in self.locations:
            url = location.get('url')
            meta = {'city': location.get('city'), 'country': location.get('country'), 'state': location.get('state')}
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)

    def parse(self, response):
        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state')
        if state == '':
            state = None
        
        rows = response.css('table.forecast-table tr')
        
        columns = [[] for _ in range(14)]

        for row in rows[1:5] + rows[13:14]:  # rows 2-5 and row 14 are irrelevant
            data = row.css('td::text').getall()
            if data:
                for i in range(14):
                    columns[i].append(data[i].strip() if i < len(data) else '')

        weather_conditions = [[] for _ in range(14)]
        for row in rows:
            imgs = row.xpath('td/img')
            for i, img in enumerate(imgs):
                title = img.xpath('@title').get()
                weather_conditions[i].append(title.strip() if title else '')


        for i in range(14):
            item = DayForecastItem(
                country=country,
                state=state,
                city=city,
                weather_condition=weather_conditions[i][0] if i < len(weather_conditions) else '',                
                temp_high=columns[i][2].replace('°', '') if len(columns[i]) > 2 else '',
                temp_low=columns[i][3].replace('°', '') if len(columns[i]) > 3 else '',
                precipitation=columns[i][4].replace('%', '') if len(columns[i]) > 4 else '',
                wind=None,
                source='MeteoBlue'
            )
            yield item
