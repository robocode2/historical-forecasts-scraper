from datetime import datetime, timedelta, timezone
import pytest
from tests.integration.base_integration_test import BaseIntegrationTest
from weatherscraper.items import DayForecastItem
from weatherscraper.spiders.meteoblue_spider import MeteoblueSpider


class TestMeteoblue(BaseIntegrationTest):
    spider_class = MeteoblueSpider
    url = 'https://www.meteoblue.com/en/weather/14-days/rome_italy_3169070'
    city = 'Rome'
    country = 'Italy'
    state = ''
    
    @pytest.fixture
    def expected_forecast_data(self):
        current_date = datetime.now(timezone.utc)
        # yes here too I had to make amounts floats 
        forecast_data = [
        {'temp_high': '22', 'temp_low': '12', 'precipitation_chance': '0', 'precipitation_amount': 0.14, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Mixed with showers', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '15', 'precipitation_chance': '10', 'precipitation_amount': 1.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Mostly cloudy with occasional rain', 'source': 'MeteoBlue'},
        {'temp_high': '24', 'temp_low': '17', 'precipitation_chance': '90', 'precipitation_amount': 30.4, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Showers, thunderstorms likely', 'source': 'MeteoBlue'},
        {'temp_high': '25', 'temp_low': '19', 'precipitation_chance': '30', 'precipitation_amount': 0.9, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Showers, thunderstorms likely', 'source': 'MeteoBlue'},
        {'temp_high': '25', 'temp_low': '19', 'precipitation_chance': '70', 'precipitation_amount': 2.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Mostly cloudy with occasional rain', 'source': 'MeteoBlue'},
        {'temp_high': '24', 'temp_low': '17', 'precipitation_chance': '10', 'precipitation_amount': 0.7, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Mixed with showers', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '15', 'precipitation_chance': '20', 'precipitation_amount': 0.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Partly cloudy', 'source': 'MeteoBlue'},
        {'temp_high': '24', 'temp_low': '15', 'precipitation_chance': '35', 'precipitation_amount': 0.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '24', 'temp_low': '15', 'precipitation_chance': '20', 'precipitation_amount': 0.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '16', 'precipitation_chance': '20', 'precipitation_amount': 0.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '16', 'precipitation_chance': '20', 'precipitation_amount': 0.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '15', 'precipitation_chance': '30', 'precipitation_amount': 0.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '15', 'precipitation_chance': '40', 'precipitation_amount': 0.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '22', 'temp_low': '15', 'precipitation_chance': '40', 'precipitation_amount': 0.0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear, cloudless sky', 'source': 'MeteoBlue'},
        ]


        return [
            DayForecastItem(
                country=self.country,
                state=self.state,
                city=self.city,
                date=current_date,
                day=current_date + timedelta(days=i),
                **data 
            ) for i, data in enumerate(forecast_data)
        ]
        
        
