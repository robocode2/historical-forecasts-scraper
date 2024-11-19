from datetime import datetime, timedelta, timezone
import scrapy
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import load_locations


class MeteoprogSpider(scrapy.Spider):
    name = "MeteoProg"
    MAX_FORECAST_DAYS = 14 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("MeteoProg")

    def start_requests(self):
        for location in self.locations:
            url = location.get('url')
            meta = {
                'city': location.get('city'),
                'country': location.get('country'),
                'state': location.get('state')
            }
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)

    def parse(self, response):
        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state')
        current_date = datetime.now(timezone.utc)

        wind_speeds = self._extract_wind_speeds(response)
        humidity = self._extract_humidity(response)
        precipitation_chances = self._extract_precipitation_chances(response)
        precipitation_amounts = self._extract_precipitation_amounts(response)
        weather_descriptions = self._extract_weather_descriptions(response)
        forecast_days = response.xpath('//div[contains(@class, "swiper-slide")]')

        actual_available_forecasts = len(weather_descriptions)

        temp_max, temp_min = self._extract_temperatures(forecast_days)

        for i in range(actual_available_forecasts):
            yield DayForecastItem(
                country=country,
                state=state,
                city=city,
                temp_high=temp_min[i] if i < len(temp_min) else None, # the website has a bug, it swaps max/min
                temp_low=temp_max[i] if i < len(temp_max) else None,
                precipitation_chance=precipitation_chances[i],
                precipitation_amount=float(precipitation_amounts[i]) if i < len(precipitation_amounts) else None,
                humidity=humidity[i] if i < len(humidity) else None,
                wind_speed=self._convert_wind_speed(wind_speeds[i]),
                weather_condition=weather_descriptions[i],
                source='MeteoProg',
                collection_date=current_date,
                forecasted_day=current_date + timedelta(days=i)
            )

    # Helper Methods
    def _extract_wind_speeds(self, response):
        return [
            response.css(f'#weather-temp-graph-week > div > div > div.item-table > ul.wind-speed-list > li:nth-child({i}) > span::text').get()
            for i in range(1, self.MAX_FORECAST_DAYS + 1)
        ]

    def _extract_humidity(self, response):
        humidity_elements = response.xpath('//*[@id="weather-temp-graph-week"]/div/div/div[2]/ul[2]/li/span[1]/text()').getall()
        return [h.strip().replace('%', '') for h in humidity_elements]

    def _extract_precipitation_chances(self, response):
        chance_elements = response.css('#weather-temp-graph-week > div > div > div.item-table > ul:nth-child(4) > li > span:first-child::text').getall()
        chances = [chance.strip() for chance in chance_elements]
        chances.extend([None] * (self.MAX_FORECAST_DAYS - len(chances)))
        return chances

    def _extract_precipitation_amounts(self, response):
        amount_elements = response.xpath('//*[@id="weather-temp-graph-week"]/div/div/div[2]/ul[5]/li/span[1]/text()').getall()
        return [amount.strip().replace(' mm', '') for amount in amount_elements]

    def _extract_weather_descriptions(self, response):
        weather_elements = response.xpath('/html/body/div[4]/main/article/section[2]/div/div[3]/div/div/div[3]/div[2]')
        return [
            ', '.join(element.xpath('./@title').get().split(', ')[1:]) 
            for element in weather_elements if element.xpath('./@title').get()
        ]

    def _extract_temperatures(self, forecast_days):
        temp_max = []
        temp_min = []

        for day in forecast_days:
            max_temp = day.xpath('.//div[contains(@class, "temperature-max")]/h6/text()').get()
            min_temp = day.xpath('.//div[contains(@class, "temperature-min")]/h6/text()').get()

            temp_max.append(max_temp.strip().replace('°', '').replace('+', '').replace('C', '') if max_temp else '')
            temp_min.append(min_temp.strip().replace('°', '').replace('+', '').replace('C', '') if min_temp else '')

        return temp_max, temp_min

    def _convert_wind_speed(self, wind_speed):
        return float(wind_speed) * 3.6 if wind_speed else None
