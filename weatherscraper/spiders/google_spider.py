import scrapy
from scrapy.crawler import CrawlerProcess

class GoogleSpider(scrapy.Spider):
    name = 'google'
    start_urls = ['https://www.google.com/search?q=weather+berlin']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0'
    }

    def parse(self, response):
        weather_divs = response.css('div.wob_df')

        for weather_div in weather_divs:
            day = weather_div.css('div.Z1VzSb::text').get()
            weather_condition = weather_div.css('img::attr(alt)').get()
            temp_high = weather_div.css('div.gNCp2e > span.wob_t::text').get()
            temp_low = weather_div.css('div.QrNVmd > span.wob_t::text').get()

            yield {
                'day': day,
                'weather_condition': weather_condition,
                'temp_high': temp_high,
                'temp_low': temp_low
            }

# To run the spider, you can uncomment the lines below and run this file directly.

# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(WeatherSpider)
#     process.start()
