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
        
        return item
        
"""    commit this separately     # Check if item['date'] is equal to item['day']
        if item['date'] == item['day']:
            # Ignore setting the date
            return
        else:
            return item """
            
import psycopg2
from scrapy.exceptions import DropItem
from .settings import DATABASE_URL

class PostgreSQLPipeline:
   def open_spider(self, spider):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor()

   def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
 
   def process_item(self, item, spider):
        if spider.name == 'TheWeatherChannel':
            try:
                # Insert City if not exists
                self.cursor.execute("""
                    INSERT INTO City (name)
                    SELECT %s
                    WHERE NOT EXISTS (SELECT 1 FROM City WHERE name = %s)
                    RETURNING id
                """, (item['city'], item['city']))
    
                city_result = self.cursor.fetchone()

                if city_result:
                    city_id = city_result[0]
                else:
                    # Fetch city_id if it already exists
                    self.cursor.execute("SELECT id FROM City WHERE name = %s", (item['city'],))
                    city_id = self.cursor.fetchone()[0]  # Assuming the city exists, fetch its id


                # Insert Country if not exists
                self.cursor.execute("""
                    INSERT INTO Country (name)
                    SELECT %s
                    WHERE NOT EXISTS (SELECT 1 FROM Country WHERE name = %s)
                    RETURNING id
                """, (item['country'], item['country']))
    
                country_result = self.cursor.fetchone()

                if country_result:
                    country_id = country_result[0]
                else:
                    # Fetch country if it already exists
                    self.cursor.execute("SELECT id FROM Country WHERE name = %s", (item['country'],))
                    country_id = self.cursor.fetchone()[0]  # Assuming the country exists, fetch its id



                # Insert Forecast
                self.cursor.execute("""
                    INSERT INTO Forecast (city_id, country_id, date, day, precipitation, state, temp_high, temp_low, weather_condition, wind)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    city_id,
                    country_id,
                    item['date'],
                    item['day'],
                    item['precipitation'],
                    item['state'],
                    item['temp_high'],
                    item['temp_low'],
                    item['weather_condition'],
                    item['wind']
                ))
                self.connection.commit()
            except psycopg2.Error as e:
                self.connection.rollback()
                raise DropItem(f"Error processing item: {e}")
            return item
        else:
            return item
            
            

    