# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DayForecastItem(scrapy.Item):
   source = scrapy.Field()
   city = scrapy.Field()
   state = scrapy.Field()
   country = scrapy.Field()
   date = scrapy.Field()
   day = scrapy.Field()
   weather_condition = scrapy.Field()
   temp_high = scrapy.Field()
   temp_low = scrapy.Field()
   precipitation_chance = scrapy.Field()
   precipitation_amount = scrapy.Field()
   humidity = scrapy.Field()
   wind_speed = scrapy.Field()
pass

