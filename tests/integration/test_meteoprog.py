from datetime import datetime, timedelta, timezone
import pytest
from tests.integration.base_integration_test import BaseIntegrationTest
from weatherscraper.spiders.meteoprog_spider import MeteoprogSpider
from weatherscraper.items import DayForecastItem

class TestMeteoprog(BaseIntegrationTest):
    spider_class = MeteoprogSpider
    url = 'https://www.meteoprog.com/review/Berlin/'
    city = 'Berlin'
    country = 'Germany'
    state = ''
    
    @pytest.fixture
    def expected_forecast_data(self):
        current_date = datetime.now(timezone.utc)
        # TODOX it's strange I had to precipitation amount to floats and wind_speed is 11 !
        forecast_data = [
        {'temp_high': '9', 'temp_low': '14', 'precipitation_chance': '0', 'precipitation_amount': 0.0, 'humidity': '67', 'wind_speed': 11, 'weather_condition': 'cloudy, clear at times, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '8', 'temp_low': '15', 'precipitation_chance': '0', 'precipitation_amount': 0.0, 'humidity': '76', 'wind_speed': 14, 'weather_condition': 'cloudy, clear at times, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '13', 'temp_low': '19', 'precipitation_chance': '0', 'precipitation_amount': 0.0, 'humidity': '71', 'wind_speed': 14, 'weather_condition': 'cloudy, clear at times, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '15', 'temp_low': '18', 'precipitation_chance': '40', 'precipitation_amount': 0.6, 'humidity': '82', 'wind_speed': 11, 'weather_condition': 'cloudy, light rain', 'source': 'MeteoProg'},
        {'temp_high': '13', 'temp_low': '19', 'precipitation_chance': '30', 'precipitation_amount': 0.0, 'humidity': '73', 'wind_speed': 18, 'weather_condition': 'overcast, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '14', 'temp_low': '13', 'precipitation_chance': '20', 'precipitation_amount': 0.6, 'humidity': '78', 'wind_speed': 22, 'weather_condition': 'overcast, light rain', 'source': 'MeteoProg'},
        {'temp_high': '8', 'temp_low': '12', 'precipitation_chance': '20', 'precipitation_amount': 0.0, 'humidity': '76', 'wind_speed': 14, 'weather_condition': 'light cloud, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '6', 'temp_low': '11', 'precipitation_chance': '30', 'precipitation_amount': 2.5, 'humidity': '80', 'wind_speed': 22, 'weather_condition': 'cloudy, rain', 'source': 'MeteoProg'},
        {'temp_high': '8', 'temp_low': '15', 'precipitation_chance': '20', 'precipitation_amount': 0.0, 'humidity': '51', 'wind_speed': 11, 'weather_condition': 'cloudy, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '6', 'temp_low': '16', 'precipitation_chance': '30', 'precipitation_amount': 0.0, 'humidity': '57', 'wind_speed': 11, 'weather_condition': 'overcast, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '7', 'temp_low': '18', 'precipitation_chance': None, 'precipitation_amount': 0.0, 'humidity': '57', 'wind_speed': 4, 'weather_condition': 'variable cloud, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '7', 'temp_low': '17', 'precipitation_chance': None, 'precipitation_amount': 0.0, 'humidity': '58', 'wind_speed': 14, 'weather_condition': 'clear, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '7', 'temp_low': '15', 'precipitation_chance': None, 'precipitation_amount': 0.0, 'humidity': '52', 'wind_speed': 22, 'weather_condition': 'clear, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '5', 'temp_low': '14', 'precipitation_chance': None, 'precipitation_amount': 0.0, 'humidity': '48', 'wind_speed': 25, 'weather_condition': 'clear, no precipitation', 'source': 'MeteoProg'},
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

