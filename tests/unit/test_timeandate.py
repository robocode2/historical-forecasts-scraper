from datetime import datetime, timedelta, timezone
from tests.unit.base_unit_test import BaseUnitTest
from weatherscraper.items import DayForecastItem
from weatherscraper.spiders.timeanddate_spider import TimeAndDateSpider


class TestTimeAndDateSpider(BaseUnitTest):
    spider_class = TimeAndDateSpider
    url = 'https://www.timeanddate.com/weather/australia/sydney/ext'
    city = 'Sydney'
    country = 'Australia'
    state = ''
    
    @property
    def expected_items(self):
        current_date = datetime(2024, 10, 8, tzinfo=timezone.utc)  # Fixed date to match the saved HTML page #precipitation amount, wind speed, and sometimes temp

        forecast_data = [
            {'temp_high': '17', 'temp_low': '14', 'precipitation_chance': '45', 'precipitation_amount': 1.0, 'humidity': '59', 'wind_speed': 14, 'weather_condition': 'Sprinkles early. Overcast.', 'source': 'TimeAndDate'},
            {'temp_high': '24', 'temp_low': '12', 'precipitation_chance': '19', 'precipitation_amount': 1.0, 'humidity': '45', 'wind_speed': 25, 'weather_condition': 'Sprinkles early. Broken clouds.', 'source': 'TimeAndDate'},
            {'temp_high': '22', 'temp_low': '16', 'precipitation_chance': '12', 'precipitation_amount': 0.5, 'humidity': '57', 'wind_speed': 14, 'weather_condition': 'Isolated tstorms late. Mostly cloudy.', 'source': 'TimeAndDate'},
            {'temp_high': '18', 'temp_low': '14', 'precipitation_chance': '52', 'precipitation_amount': 2.3, 'humidity': '57', 'wind_speed': 35, 'weather_condition': 'Sprinkles. Cloudy.', 'source': 'TimeAndDate'},
            {'temp_high': '20', 'temp_low': '13', 'precipitation_chance': '20', 'precipitation_amount': 0.8, 'humidity': '48', 'wind_speed': 19, 'weather_condition': 'Sprinkles early. Breaks of sun late.', 'source': 'TimeAndDate'},
            {'temp_high': '24', 'temp_low': '12', 'precipitation_chance': '0', 'precipitation_amount': None, 'humidity': '42', 'wind_speed': 17, 'weather_condition': 'Overcast.', 'source': 'TimeAndDate'},
            {'temp_high': '26', 'temp_low': '16', 'precipitation_chance': '62', 'precipitation_amount': 3.8, 'humidity': '44', 'wind_speed': 17, 'weather_condition': 'Isolated tstorms late. Overcast.', 'source': 'TimeAndDate'},
            {'temp_high': '21', 'temp_low': '17', 'precipitation_chance': '73', 'precipitation_amount': 10.4, 'humidity': '73', 'wind_speed': 9, 'weather_condition': 'A few tstorms. Cloudy.', 'source': 'TimeAndDate'},
            {'temp_high': '21', 'temp_low': '18', 'precipitation_chance': '52', 'precipitation_amount': 1.0, 'humidity': '72', 'wind_speed': 12, 'weather_condition': 'Isolated tstorms. Broken clouds.', 'source': 'TimeAndDate'},
            {'temp_high': '22', 'temp_low': '19', 'precipitation_chance': '82', 'precipitation_amount': 23.4, 'humidity': '93', 'wind_speed': 14, 'weather_condition': 'Thunderstorms. Overcast.', 'source': 'TimeAndDate'},
            {'temp_high': '22', 'temp_low': '19', 'precipitation_chance': '74', 'precipitation_amount': 7.4, 'humidity': '86', 'wind_speed': 6, 'weather_condition': 'Isolated tstorms. Cloudy.', 'source': 'TimeAndDate'},
            {'temp_high': '22', 'temp_low': '19', 'precipitation_chance': '19', 'precipitation_amount': 0.8, 'humidity': '77', 'wind_speed': 17, 'weather_condition': 'Isolated tstorms late. Afternoon clouds.', 'source': 'TimeAndDate'},
            {'temp_high': '22', 'temp_low': '19', 'precipitation_chance': '48', 'precipitation_amount': 0.5, 'humidity': '71', 'wind_speed': 19, 'weather_condition': 'Sprinkles late. Broken clouds.', 'source': 'TimeAndDate'},
            {'temp_high': '22', 'temp_low': '21', 'precipitation_chance': '41', 'precipitation_amount': 0.3, 'humidity': '70', 'wind_speed': 16, 'weather_condition': 'Sprinkles early. Breaks of sun late.', 'source': 'TimeAndDate'},
            {'temp_high': '20', 'temp_low': '18', 'precipitation_chance': '53', 'precipitation_amount': 2.0, 'humidity': '59', 'wind_speed': 40, 'weather_condition': 'Sprinkles. Mostly cloudy.', 'source': 'TimeAndDate'},
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