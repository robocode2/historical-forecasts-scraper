from datetime import timedelta
import pytest
from scrapy.http import HtmlResponse, Request
import psycopg2
from psycopg2.extras import DictCursor
from weatherscraper.pipelines import PostgreSQLPipeline

class BaseIntegrationTest:
    spider_class = None
    url = '' 
    city = ''
    country = ''
    state = ''
    expected_forecast_data = [] 

    @pytest.fixture
    def spider(self):
        return self.spider_class()


    @pytest.fixture(scope="class")
    def html_response(self):
        request = Request(url=self.url, meta={
            'city': self.city,
            'country': self.country,
            'state': self.state
        })

        with open(f'tests/mocks/{self.spider_class.__name__.lower()}.html', 'r', encoding='utf-8') as f:
            body = f.read()

        return HtmlResponse(url=self.url, body=body.encode('utf-8'), encoding='utf-8', request=request) 
    
    @pytest.fixture
    def db_connection(self):
        try:
            connection = psycopg2.connect(
                host='localhost',
                database='testforecastsdb',
                user='rabiecode',
                password='IDnowLOV123!',
                port='5432'
            )
            yield connection
        except psycopg2.OperationalError as e:
            pytest.fail("Database connection failed")
        finally:
            if connection:
                connection.close()

    @pytest.fixture
    def db_pipeline(self):
        pipeline = PostgreSQLPipeline()
        pipeline.open_spider(None)  
        yield pipeline  
        pipeline.close_spider(None) 

    @pytest.fixture(autouse=True)
    def clean_database(self, db_connection):
        with db_connection.cursor() as cursor:
            cursor.execute("DELETE FROM Forecast;")
            cursor.execute("DELETE FROM City;")
            cursor.execute("DELETE FROM Country;")
            cursor.execute("DELETE FROM Source;")
        db_connection.commit()

    def parse_mock_response(self, spider, response):
        request = Request(self.url)
        response = HtmlResponse(url=self.url, request=request, body=response, encoding='utf-8')
        return list(spider.parse(response))

    def assert_value(self, expected_value, actual_value):
        if expected_value is None:
            assert actual_value is None
        else:
            assert actual_value is not None
            expected_str = str(expected_value)
            actual_str = str(actual_value)
        
            assert actual_str == expected_str, f"Expected '{expected_str}', but got '{actual_str}'"

        
    def verify_database_insertion(self, db_connection, expected_forecast_data):
        with db_connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
                SELECT c.id, co.id, s.id
                FROM City c
                JOIN Country co ON co.name = %s
                JOIN Source s ON s.name = %s
                WHERE c.name = %s
            """, (expected_forecast_data[0]['country'], expected_forecast_data[0]['source'], expected_forecast_data[0]['city']))
            
            ids = cursor.fetchone()
            assert ids is not None, "City, country, or source not found in the database"
            city_id, country_id, source_id = ids

            cursor.execute("""
                SELECT f.*
                FROM Forecast f
                WHERE f.city_id = %s AND f.source_id = %s
                ORDER BY f.collection_date ASC
            """, (city_id, source_id))
            
            db_forecasts = cursor.fetchall()
            assert db_forecasts is not None, f"No forecast data found for city {expected_forecast_data[0]['city']} and source {expected_forecast_data[0]['source']}"
            assert len(db_forecasts) == len(expected_forecast_data), "Mismatch in number of forecast items"            
           
            previous_day = None
            for db_forecast, expected_forecast in zip(db_forecasts, expected_forecast_data):
                for field in ['temp_high', 'temp_low', 'precipitation_chance', 'precipitation_amount', 'wind_speed',  'humidity','weather_condition']:
                    self.assert_value(expected_forecast[field], db_forecast[field])
                
                db_day = db_forecast['forecasted_day'] 
                if previous_day:
                    assert db_day.date() == previous_day.date() + timedelta(days=1), f"Day {db_day} is not 1 day after {previous_day}"
                previous_day = db_day
                    
        
    def test__integration(self, expected_forecast_data, db_connection, db_pipeline, html_response):
        spider = self.spider_class()
        scraped_items = list(spider.parse(html_response))

        for scraped in scraped_items:
            db_pipeline.process_item(scraped, spider)

        self.verify_database_insertion(db_connection, expected_forecast_data)
                    
