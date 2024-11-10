from datetime import datetime, timedelta, timezone
from tests.unit.base_unit_test import BaseUnitTest
from weatherscraper.items import DayForecastItem
from weatherscraper.spiders.meteoblue_spider import MeteoBlueSpider


class TestMeteoblueSpider(BaseUnitTest):
    spider_class = MeteoBlueSpider
    url = 'https://www.meteoblue.com/en/weather/14-days/rome_italy_3169070'
    city = 'Rome'
    country = 'Italy'
    state = ''
    
    @property
    def expected_items(self):
        current_date = datetime(2024, 10, 6, tzinfo=timezone.utc)  # Fixed date to match the saved HTML page

        forecast_data = [
        {'temp_high': '22', 'temp_low': '12', 'precipitation_chance': '0', 'precipitation_amount': 0.14, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Mixed with showers', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '15', 'precipitation_chance': '10', 'precipitation_amount': 1, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Mostly cloudy with occasional rain', 'source': 'MeteoBlue'},
        {'temp_high': '24', 'temp_low': '17', 'precipitation_chance': '90', 'precipitation_amount': 30.4, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Showers, thunderstorms likely', 'source': 'MeteoBlue'},
        {'temp_high': '25', 'temp_low': '19', 'precipitation_chance': '30', 'precipitation_amount': 0.9, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Showers, thunderstorms likely', 'source': 'MeteoBlue'},
        {'temp_high': '25', 'temp_low': '19', 'precipitation_chance': '70', 'precipitation_amount': 2, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Mostly cloudy with occasional rain', 'source': 'MeteoBlue'},
        {'temp_high': '24', 'temp_low': '17', 'precipitation_chance': '10', 'precipitation_amount': 0.7, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Mixed with showers', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '15', 'precipitation_chance': '20', 'precipitation_amount': 0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Partly cloudy', 'source': 'MeteoBlue'},
        {'temp_high': '24', 'temp_low': '15', 'precipitation_chance': '35', 'precipitation_amount': 0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '24', 'temp_low': '15', 'precipitation_chance': '20', 'precipitation_amount': 0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '16', 'precipitation_chance': '20', 'precipitation_amount': 0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '16', 'precipitation_chance': '20', 'precipitation_amount': 0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '15', 'precipitation_chance': '30', 'precipitation_amount': 0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '23', 'temp_low': '15', 'precipitation_chance': '40', 'precipitation_amount': 0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear and few clouds', 'source': 'MeteoBlue'},
        {'temp_high': '22', 'temp_low': '15', 'precipitation_chance': '40', 'precipitation_amount': 0, 'humidity': None, 'wind_speed': None, 'weather_condition': 'Clear, cloudless sky', 'source': 'MeteoBlue'},
        ]


        return [
            DayForecastItem(
                country=self.country,
                state=self.state,
                city=self.city,
                collection_date=current_date,
                forecasted_day=current_date + timedelta(days=i),
                **data 
            ) for i, data in enumerate(forecast_data)
        ]