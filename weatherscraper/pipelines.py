# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from scrapy.exceptions import DropItem

class PostgreSQLPipeline:
   def open_spider(self, spider):
        self.connection = psycopg2.connect()
        self.cursor = self.connection.cursor()

   def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
 
   def process_item(self, item, spider):
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


                 # Insert City if not exists
                self.cursor.execute("""
                    INSERT INTO Source (name)
                    SELECT %s
                    WHERE NOT EXISTS (SELECT 1 FROM Source WHERE name = %s)
                    RETURNING id
                """, (item['source'], item['source']))
    
                source_result = self.cursor.fetchone()

                if source_result:
                    source_id = source_result[0]
                else:
                    # Fetch source if it already exists
                    self.cursor.execute("SELECT id FROM Source WHERE name = %s", (item['source'],))
                    source_id = self.cursor.fetchone()[0]  # Assuming the city exists, fetch its id

                # Insert Forecast
                self.cursor.execute("""
                    INSERT INTO Forecast (source_id, city_id, country_id, state, date, day, precipitation_chance, precipitation_amount, temp_high, temp_low, wind_speed, humidity, weather_condition)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    source_id,
                    city_id,
                    country_id,
                    item['state'],
                    item['date'],
                    item['day'],
                    item['precipitation_chance'],
                    item['precipitation_amount'],
                    item['temp_high'],
                    item['temp_low'],
                    item['wind_speed'],
                    item['humidity'],
                    item['weather_condition']
                ))
                self.connection.commit()
            except psycopg2.Error as e:
                self.connection.rollback()
                raise DropItem(f"Error processing item: {e}")
            return item
            
            

    

    