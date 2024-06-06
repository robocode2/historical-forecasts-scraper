import scrapy
from scrapy.crawler import CrawlerProcess
from weatherscraper.items import DayForecastItem;

class WeatherSpider(scrapy.Spider):
    name = "weather"
    start_urls = [
        "https://weather.com/weather/tenday/l/153e65f344ab389e17703aae99cf18a182265e8095831d55ddfcfc6c5aa9a91c#detailIndex5"
    ]
    
    def parse(self, response):
        for day in response.css('summary.Disclosure--Summary--3GiL4'):
                day_forecast = DayForecastItem()
                day_forecast['day'] = day.css('h2.DetailsSummary--daypartName--kbngc::text').get()
                day_forecast['weather_condition'] = day.css('div.DetailsSummary--condition--2JmHb span::text').get()
                day_forecast['temp_high'] = day.css('span.DetailsSummary--highTempValue--3PjlX::text').get()
                day_forecast['temp_low'] = day.css('span.DetailsSummary--lowTempValue--2tesQ::text').get()
                day_forecast['precipitation'] = day.css('div.DetailsSummary--precip--1a98O span::text').get()
                day_forecast['wind'] = day.css('span[data-testid="Wind"] span:nth-child(2)::text').extract_first()
                print(day_forecast)
                yield day_forecast
       
