import scrapy

class HeadersSpider(scrapy.Spider):
    name = "headers"
    allowed_domains = ["httpbin.io"]
    start_urls = ["https://httpbin.io/user-agent", "https://httpbin.io/user-agent", "https://httpbin.io/user-agent"]

    def parse(self, response):
        print(f'RESPONSE: {response.text}')