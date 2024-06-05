import scrapy
from scrapy.crawler import CrawlerProcess

class WeatherSpider(scrapy.Spider):
    name = "weather"
    start_urls = [
        "https://weather.com/weather/tenday/l/153e65f344ab389e17703aae99cf18a182265e8095831d55ddfcfc6c5aa9a91c#detailIndex5"
    ]

    def parse(self, response):
        for day in response.css('summary.Disclosure--Summary--3GiL4'):
            day_data = {
                'day': day.css('h2.DetailsSummary--daypartName--kbngc::text').get(),
                'weather_condition': day.css('div.DetailsSummary--condition--2JmHb span::text').get(),
                'temp_high': day.css('span.DetailsSummary--highTempValue--3PjlX::text').get(),
                'temp_low': day.css('span.DetailsSummary--lowTempValue--2tesQ::text').get(),
                'precipitation': day.css('div.DetailsSummary--precip--1a98O span::text').get(),
                'wind': day.css('div.DetailsSummary--wind--1tv7t span.Wind--windWrapper--3Ly7c::text').getall()
            }
            print(day_data)
            yield day_data
