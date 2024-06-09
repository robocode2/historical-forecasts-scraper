# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime, timedelta

class WeatherPipeline:
    def __init__(self):
        self.current_city = None
        self.start_date = None
        self.date_delta = timedelta(days=1)

    def process_item(self, item, spider):
        # Remove White Space in Weather Condition
        item['weather_condition'] = item['weather_condition'].lower().replace(' ', '_')

        # Check if we are processing a new city
        if self.current_city != item['city']:
            self.current_city = item['city']
            self.start_date = datetime.strptime('2024-06-09', '%Y-%m-%d')  # Reset start date for new city
        
        # Set the date for the item
        item['day'] = self.start_date.strftime('%Y-%m-%d')
        
        # Increment the start date for the next item in the same city
        self.start_date += self.date_delta

        return item