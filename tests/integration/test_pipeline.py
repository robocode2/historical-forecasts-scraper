from scrapy import Spider

from weatherscraper.pipelines import PostgreSQLPipeline

def test_pipeline():
    pipeline = PostgreSQLPipeline()
    spider = Spider('MeteoProg')
    pipeline.open_spider(spider)
    
    item = {
        'city': 'Berlin',
        'country': 'Germany',
        'state': 'Berlin',
        'collection_date': '2024-10-06',
        'forecasted_day': '2024-10-06',
        'precipitation_chance': '40',
        'precipitation_amount': '0.0',
        'temp_high': '14',
        'temp_low': '13',
        'wind_speed': '21',
        'humidity': '75',
        'weather_condition': 'overcast, light rain',
        'source': 'MeteoProg'
    }
    
    pipeline.process_item(item, spider)
    pipeline.close_spider(spider)