from datetime import datetime, timedelta, timezone
import pytest
from tests.integration.base_integration_test import BaseIntegrationTest
from weatherscraper.items import DayForecastItem
from weatherscraper.spiders.weather_spider import TheWeatherChannelSpider


class TestTheWeatherChannel(BaseIntegrationTest):
    spider_class = TheWeatherChannelSpider
    url = 'https://weather.com/weather/tenday/l/39.90,116.41'
    city = 'Beijing'
    country = 'China'
    state = ''
    
    @pytest.fixture
    def expected_forecast_data(self):
        current_date = datetime.now(timezone.utc)

        forecast_data = [
            {'temp_high': None, 'temp_low': '13', 'precipitation_chance': '7', 'precipitation_amount': None, 'humidity': '89', 'wind_speed': '8', 'weather_condition': 'Mostly Cloudy Night', 'source': 'TheWeatherChannel'},
            {'temp_high': '20', 'temp_low': '13', 'precipitation_chance': '52', 'precipitation_amount': None, 'humidity': '76', 'wind_speed': '9', 'weather_condition': 'Scattered Showers', 'source': 'TheWeatherChannel'},
            {'temp_high': '24', 'temp_low': '13', 'precipitation_chance': '9', 'precipitation_amount': None, 'humidity': '69', 'wind_speed': '9', 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '20', 'temp_low': '10', 'precipitation_chance': '6', 'precipitation_amount': None, 'humidity': '39', 'wind_speed': '17', 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '19', 'temp_low': '12', 'precipitation_chance': '1', 'precipitation_amount': None, 'humidity': '52', 'wind_speed': '10', 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '16', 'temp_low': '10', 'precipitation_chance': '15', 'precipitation_amount': None, 'humidity': '58', 'wind_speed': '12', 'weather_condition': 'Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '19', 'temp_low': '4', 'precipitation_chance': '16', 'precipitation_amount': None, 'humidity': '41', 'wind_speed': '14', 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '13', 'temp_low': '2', 'precipitation_chance': '0', 'precipitation_amount': None, 'humidity': '33', 'wind_speed': None, 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '12', 'temp_low': '2', 'precipitation_chance': '6', 'precipitation_amount': None, 'humidity': '38', 'wind_speed': '12', 'weather_condition': 'Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '13', 'temp_low': '3', 'precipitation_chance': '23', 'precipitation_amount': None, 'humidity': '62', 'wind_speed': '9', 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '18', 'temp_low': '6', 'precipitation_chance': '4', 'precipitation_amount': None, 'humidity': '58', 'wind_speed': '9', 'weather_condition': 'Mostly Sunny', 'source': 'TheWeatherChannel'},
            {'temp_high': '19', 'temp_low': '7', 'precipitation_chance': '2', 'precipitation_amount': None, 'humidity': '51', 'wind_speed': '10', 'weather_condition': 'Sunny', 'source': 'TheWeatherChannel'},
            {'temp_high': '19', 'temp_low': '7', 'precipitation_chance': '1', 'precipitation_amount': None, 'humidity': '50', 'wind_speed': '9', 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '19', 'temp_low': '6', 'precipitation_chance': '7', 'precipitation_amount': None, 'humidity': '49', 'wind_speed': '10', 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
            {'temp_high': '17', 'temp_low': '7', 'precipitation_chance': '14', 'precipitation_amount': None, 'humidity': '54', 'wind_speed': '8', 'weather_condition': 'Partly Cloudy', 'source': 'TheWeatherChannel'},
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
        
