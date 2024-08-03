import scrapy
 
class ScraperSpider(scrapy.Spider):
    name = "proxies"
 
    def start_requests(self):
        urls = [
            'https://httpbin.org/ip',
            'http://ident.me/', 
			'https://api.ipify.org?format=json',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        print('IP address: %s' % response.text)