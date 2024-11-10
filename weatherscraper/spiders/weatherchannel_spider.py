import scrapy
from datetime import datetime, timedelta, timezone
from scrapy_selenium import SeleniumRequest
from weatherscraper.items import DayForecastItem
from weatherscraper.utils import load_locations


class TheWeatherChannelSpider(scrapy.Spider):
    name = "TheWeatherChannel"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = load_locations("TheWeatherChannel")

    def start_requests(self):
        for location in self.locations:
            url = location.get('url') + '?unit=m'
            meta = {
                'city': location.get('city'),
                'country': location.get('country'),
                'state': location.get('state')
            }
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10, meta=meta)

    def parse(self, response):
        city = response.meta.get('city')
        country = response.meta.get('country')
        state = response.meta.get('state') or ''
        current_date = datetime.now(timezone.utc)

        for day_index in range(15):
            day_selector = f'//*[@id="detailIndex{day_index}"]'

            yield DayForecastItem(
            country=country,
            state=state,
            city=city,
            source='TheWeatherChannel',
            collection_date=current_date,
            forecasted_day=current_date + timedelta(days=day_index),
            humidity=self._extract_humidity(response, day_selector),
            wind_speed=self._extract_wind_speed(response, day_selector),
            weather_condition=self._extract_weather_condition(response, day_selector, day_index),
            precipitation_chance=self._extract_precipitation_chance(response, day_selector, day_index),
            precipitation_amount=None,
            temp_high=self._extract_temperature(response, day_selector, "high"),
            temp_low=self._extract_temperature(response, day_selector, "low")
        )


    # Helper Methods
    def _extract_humidity(self, response, day_selector):
        humidity = response.xpath(day_selector + '/div/div[2]/ul/li[1]/div/span[2]/text()').get()
        return humidity.replace('%', '').strip() if humidity else None

    def _extract_wind_speed(self, response, day_selector):
        wind_speed = response.xpath(day_selector + '/div/div[1]/div/div[3]/div[2]/span/span[2]/text()').get()
        return wind_speed or None

    def _extract_precipitation_chance(self, response, day_selector, day_index):
        if day_index == 0:
            chance = response.xpath('//*[@id="detailIndex0"]/div/div[1]/div/div[3]/div[1]/span/text()').get()
        else:
            chance = (
                response.xpath(day_selector + '/div[@class="DailyContent--precipIconBlock--LoWxx"]/span[@class="DailyContent--value--Xgh8M"]/text()').get() or
                response.xpath(day_selector + '/summary/div/div/div[3]/span[@data-testid="PercentageValue"]/text()').get()
            )
        
        return chance.replace('%', '').strip() if chance else None

    def _extract_temperature(self, response, day_selector, temp_type):
        temp_class = "DetailsSummary--highTempValue" if temp_type == "high" else "DetailsSummary--lowTempValue"
        temperature = response.xpath(day_selector + f'//*[contains(@class, "{temp_class}")]/text()').get()
        return temperature if temperature != "--" else None
    
    def _extract_weather_condition(self, response, day_selector, day_index):
        if day_index == 0:
            return response.xpath('//*[@id="detailIndex0"]/div/div[1]/div/div[2]/svg/title/text()').get()
        else:
            return response.xpath(day_selector + '/div[@class="DetailsSummary--condition--2JmHb"]/span/text()').get() or \
                   response.xpath(day_selector + '/summary/div/div/div[1]/svg/title/text()').get()

