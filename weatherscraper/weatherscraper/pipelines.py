# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from datetime import datetime, timedelta
import csv

class WeatherPipeline:
    def __init__(self):
        self.first_date = None
        self.date_delta = timedelta(days=1)
    
    def process_item(self, item, spider):
        # Remove White Space in Weather Condition
        item['weather_condition'] = item['weather_condition'].replace(' ', '-')
        
        # Enter Correct Dates
        if self.first_date is None:
            self.first_date = datetime.now().strftime('%Y-%m-%d')
        else:
            self.first_date = (datetime.strptime(self.first_date, '%Y-%m-%d') + self.date_delta).strftime('%Y-%m-%d')
        item['day'] = self.first_date
        
        # Convert Fahrenheit to Celsius and round to two decimal places
        if 'temp_high' in item and item['temp_high']:
            fahrenheit_high = float(item['temp_high'])
            celsius_high = (fahrenheit_high - 32) * 5.0/9.0
            item['temp_high'] = round(celsius_high, 2)
        
        if 'temp_low' in item and item['temp_low']:
            fahrenheit_low = float(item['temp_low'])
            celsius_low = (fahrenheit_low - 32) * 5.0/9.0
            item['temp_low'] = round(celsius_low, 2)
        
        return item