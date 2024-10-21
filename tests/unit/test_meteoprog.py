from datetime import datetime, timedelta, timezone
from tests.unit.base_unit_test import BaseUnitTest
from weatherscraper.items import DayForecastItem
from weatherscraper.spiders.meteoprog_spider import MeteoprogSpider


class TestMeteoProgSpider(BaseUnitTest):
    spider_class = MeteoprogSpider
    url = 'https://www.meteoprog.com/review/Berlin/'
    city = 'Berlin'
    country = 'Germany'
    state = ''
    
    @property
    def expected_items(self):
        current_date = datetime(2024, 10, 6, tzinfo=timezone.utc)  # Fixed date for consistency

        forecast_data = [
        {'temp_high': '9', 'temp_low': '14', 'precipitation_chance': '0', 'precipitation_amount': 0, 'humidity': '67', 'wind_speed': 10.8, 'weather_condition': 'cloudy, clear at times, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '8', 'temp_low': '15', 'precipitation_chance': '0', 'precipitation_amount': 0, 'humidity': '76', 'wind_speed': 14.4, 'weather_condition': 'cloudy, clear at times, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '13', 'temp_low': '19', 'precipitation_chance': '0', 'precipitation_amount': 0, 'humidity': '71', 'wind_speed': 14.4, 'weather_condition': 'cloudy, clear at times, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '15', 'temp_low': '18', 'precipitation_chance': '40', 'precipitation_amount': 0.6, 'humidity': '82', 'wind_speed': 10.8, 'weather_condition': 'cloudy, light rain', 'source': 'MeteoProg'},
        {'temp_high': '13', 'temp_low': '19', 'precipitation_chance': '30', 'precipitation_amount': 0, 'humidity': '73', 'wind_speed': 18.0, 'weather_condition': 'overcast, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '14', 'temp_low': '13', 'precipitation_chance': '20', 'precipitation_amount': 0.6, 'humidity': '78', 'wind_speed': 21.6, 'weather_condition': 'overcast, light rain', 'source': 'MeteoProg'},
        {'temp_high': '8', 'temp_low': '12', 'precipitation_chance': '20', 'precipitation_amount': 0, 'humidity': '76', 'wind_speed': 14.4, 'weather_condition': 'light cloud, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '6', 'temp_low': '11', 'precipitation_chance': '30', 'precipitation_amount': 2.5, 'humidity': '80', 'wind_speed': 21.6, 'weather_condition': 'cloudy, rain', 'source': 'MeteoProg'},
        {'temp_high': '8', 'temp_low': '15', 'precipitation_chance': '20', 'precipitation_amount': 0, 'humidity': '51', 'wind_speed': 10.8, 'weather_condition': 'cloudy, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '6', 'temp_low': '16', 'precipitation_chance': '30', 'precipitation_amount': 0, 'humidity': '57', 'wind_speed': 10.8, 'weather_condition': 'overcast, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '7', 'temp_low': '18', 'precipitation_chance': None, 'precipitation_amount': 0, 'humidity': '57', 'wind_speed': 3.6, 'weather_condition': 'variable cloud, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '7', 'temp_low': '17', 'precipitation_chance': None, 'precipitation_amount': 0, 'humidity': '58', 'wind_speed': 14.4, 'weather_condition': 'clear, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '7', 'temp_low': '15', 'precipitation_chance': None, 'precipitation_amount': 0, 'humidity': '52', 'wind_speed': 21.6, 'weather_condition': 'clear, no precipitation', 'source': 'MeteoProg'},
        {'temp_high': '5', 'temp_low': '14', 'precipitation_chance': None, 'precipitation_amount': 0, 'humidity': '48', 'wind_speed': 25.2, 'weather_condition': 'clear, no precipitation', 'source': 'MeteoProg'},
    ]

        return [
            DayForecastItem(
                country=self.country,
                state=self.state,
                city=self.city,
                date=current_date,
                day=current_date + timedelta(days=i),
                **data  # Unpack the dictionary into the DayForecastItem
            ) for i, data in enumerate(forecast_data)
        ]