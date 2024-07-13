# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DayForecastItem(scrapy.Item):
   country = scrapy.Field()
   state = scrapy.Field()
   city = scrapy.Field()
   date = scrapy.Field()
   day = scrapy.Field()
   weather_condition = scrapy.Field()
   temp_high = scrapy.Field()
   temp_low = scrapy.Field()
   precipitation = scrapy.Field()
   wind = scrapy.Field()
   source = scrapy.Field()
pass

