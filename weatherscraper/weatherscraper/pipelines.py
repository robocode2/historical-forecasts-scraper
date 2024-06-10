# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime, timedelta
from scrapy.exceptions import DropItem

class WeatherPipeline:
    def __init__(self):
        self.city_start_dates = {}

    def process_item(self, item, spider):
        city = item['city']
        
        # Remove White Space in Weather Condition
        item['weather_condition'] = item['weather_condition'].lower().replace(' ', '_')

        # Get the current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Set the item's date to the current date
        item['date'] = current_date
        
        # Check if this is a new city or if the city hasn't been seen before
        if city not in self.city_start_dates:
            self.city_start_dates[city] = current_date  # Set the start date for this city
        else:
            # Increment the day by one from the previous value
            prev_day = datetime.strptime(self.city_start_dates[city], '%Y-%m-%d')
            next_day = prev_day + timedelta(days=1)
            self.city_start_dates[city] = next_day.strftime('%Y-%m-%d')
        
        # Set the item's day
        item['day'] = self.city_start_dates[city]
        
        # Check if item['date'] is equal to item['day']
        if item['date'] == item['day']:
            # Ignore setting the date
            return
        else:
            return item