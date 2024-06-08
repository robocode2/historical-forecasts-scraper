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
        #item['weather_condition'] = item['weather_condition'].replace(' ', '-')
        
        # Enter Correct Dates
        if self.first_date is None:
            self.first_date = datetime.now().strftime('%Y-%m-%d')
        else:
            self.first_date = (datetime.strptime(self.first_date, '%Y-%m-%d') + self.date_delta).strftime('%Y-%m-%d')
        item['day'] = self.first_date
        
        
        return item