from datetime import timedelta
import pytest
from scrapy.http import HtmlResponse, Request

class BaseUnitTest:
    spider_class = None
    url = '' 
    city = ''
    country = ''
    state = ''

    @pytest.fixture
    def spider(self):
        return self.spider_class()

    @pytest.fixture
    def mock_response(self):
        request = Request(url=self.url, meta={
            'city': self.city,
            'country': self.country,
            'state': self.state
        })

        with open(f'tests/mocks/{self.spider_class.__name__.lower()}.html', 'r', encoding='utf-8') as f:
            body = f.read()

        return HtmlResponse(url=self.url, body=body.encode('utf-8'), encoding='utf-8', request=request)

    @property
    def expected_items(self):
        raise NotImplementedError("Subclasses must define expected_items")
    
    def test_parse(self, spider, mock_response):
        mock_response.request = type('Request', (), {'meta': {
            'city': self.city,
            'country': self.country,
            'state': self.state
        }})()

        items = list(spider.parse(mock_response))

        assert len(items) == len(self.expected_items)
        
        previous_day = None
        for expected, actual in zip(self.expected_items, items):
            print(f"Expected: {expected}, Actual: {actual}")
            assert expected['country'] == actual['country']
            assert expected['state'] == actual['state']
            assert expected['city'] == actual['city']
            if expected['temp_high'] is not None and actual['temp_high'] is not None:
                assert float(expected['temp_high']) == float(actual['temp_high'])
            else:
                assert expected['temp_high'] == actual['temp_high']  # TODOX WHAT ?! Both should be None if no temp 

            if expected['temp_low'] is not None and actual['temp_low'] is not None:
                assert float(expected['temp_low']) == float(actual['temp_low'])
            else:
                assert expected['temp_low'] == actual['temp_low']  # TODOX WHAT ? Both should be None if no temp
            assert expected['precipitation_chance'] == actual['precipitation_chance']
            assert expected['precipitation_amount'] == actual['precipitation_amount']
            assert expected['humidity'] == actual['humidity']
            assert expected['wind_speed'] == actual['wind_speed']
            assert expected['weather_condition'] == actual['weather_condition']
            assert expected['source'] == actual['source']
            
            if previous_day:
                assert actual['forecasted_day'] == previous_day + timedelta(days=1)
            previous_day = actual['forecasted_day']