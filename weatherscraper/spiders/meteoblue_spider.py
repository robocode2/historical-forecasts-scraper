from datetime import datetime, timedelta, timezone
import scrapy
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import fahrenheit_to_celsius, inch_to_mm, load_locations
import json

class MeteoBlueSpider(scrapy.Spider):
    name = "MeteoBlue"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("MeteoBlue")

    def start_requests(self):
        for location in self.locations:
            yield SeleniumRequest(
                url=location.get('url'),
                callback=self.parse,
                wait_time=10,
                meta={'city': location.get('city'), 'country': location.get('country'), 'state': location.get('state')}
            )

    def parse(self, response):
        meta_data = response.meta
        current_date = datetime.now(timezone.utc)
        
        columns = self._extract_table_data(response)
        weather_conditions = self._extract_weather_conditions(response)
        precipitation_data = self._parse_precipitation_data(response)

        for day in range(14):
            temp_high, temp_low, precipitation_amount = self._calculate_temps_and_precip(columns, precipitation_data, day, response)
            yield DayForecastItem(
                country=meta_data.get('country'),
                state=meta_data.get('state'),
                city=meta_data.get('city'),
                weather_condition=weather_conditions[day][0] if day < len(weather_conditions) and weather_conditions[day] else None,
                temp_high=temp_high,
                temp_low=temp_low,
                precipitation_chance=columns[day][4].replace('%', '') if len(columns[day]) > 4 else None,
                precipitation_amount=float(precipitation_amount) if precipitation_amount else 0.0,
                wind_speed=None,
                humidity=None,
                source='MeteoBlue',
                collection_date=current_date,
                forecasted_day=current_date + timedelta(days=day)
            )

    # Helper Methods
    def _extract_table_data(self, response):
        rows = response.css('table.forecast-table tr')
        columns = [[] for _ in range(14)]

        for row in rows[1:5] + rows[13:14]:  # Skip irrelevant rows
            data = row.css('td::text').getall()
            if data:
                for i, cell in enumerate(data):
                    if i < 14:
                        columns[i].append(cell.strip())
        return columns

    def _extract_weather_conditions(self, response):
        rows = response.css('table.forecast-table tr')
        conditions = [[] for _ in range(14)]
        
        for row in rows:
            for i, img in enumerate(row.xpath('td/img')):
                title = img.xpath('@title').get()
                if title:
                    conditions[i].append(title.strip())
        return conditions

    def _parse_precipitation_data(self, response):
        data_str = response.xpath('//*[@id="canvas_14_days_forecast_precipitations"]/@data-precipitation').get()
        
        try:
            return json.loads(data_str) if data_str else [None] * 14
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse precipitation data: {data_str}")
            return [None] * 14

    def _calculate_temps_and_precip(self, columns, precipitation_data, day, response):
        temp_unit = response.css('.h1.current-temp::text').re_first(r'°[CF]')
        
        temp_high = columns[day][2].replace('°', '') if len(columns[day]) > 2 else None
        temp_low = columns[day][3].replace('°', '') if len(columns[day]) > 3 else None
        precipitation_amount = precipitation_data[day] if day < len(precipitation_data) else None

        # Explicitly check for None rather than falsy values to handle `0`
        if temp_high is not None and temp_unit == '°F':
            temp_high = fahrenheit_to_celsius(temp_high)
        if temp_low is not None and temp_unit == '°F':
            temp_low = fahrenheit_to_celsius(temp_low)
        if precipitation_amount is not None and temp_unit == '°F':
            precipitation_amount = inch_to_mm(float(precipitation_amount))

        return temp_high, temp_low, precipitation_amount

