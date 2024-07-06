from shutil import which
import os
from dotenv import load_dotenv

load_dotenv()
# Scrapy settings for weatherscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "weatherscraper"

SPIDER_MODULES = ["weatherscraper.spiders"]
NEWSPIDER_MODULE = "weatherscraper.spiders"
LOG_LEVEL = 'ERROR'

LOCATIONS_JSON_PATH = 'weatherScraper/locations.json'

# Add Your ScrapeOps API Key
SCRAPEOPS_API_KEY= 'dbfe6e2a-857c-48ab-b04f-9c013eccbc4e'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "weatherscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "weatherscraper.middlewares.WeatherscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 900,
    
}



#SELENIUM_DRIVER_NAME = 'chrome'
#SELENIUM_DRIVER_EXECUTABLE_PATH = which("chromedriver")
#SELENIUM_DRIVER_ARGUMENTS=['-headless', "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]

# Function to configure Selenium
""" def configure_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=chrome_service, options=chrome_options)
 """
""" SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = '/root/weatherScraper/weatherscraper/weatherscraper/geckodriver'
SELENIUM_DRIVER_ARGUMENTS=[]
 """
  
""" CHROMEDRIVER_PATH = '/root/weatherScraper/weatherscraper/weatherscraper/spiders/geckodriver'
SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = CHROMEDRIVER_PATH 
SELENIUM_DRIVER_ARGUMENTS=['-headless', "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
SELENIUM_BROWSER_EXECUTABLE_PATH = os.environ.get("FIREFOX_BIN", "geckodriver")
 """
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which("chromedriver")
SELENIUM_DRIVER_ARGUMENTS = [] 
# Other Scrapy settings
ROBOTSTXT_OBEY = True


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

EXTENSIONS = {
        'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
        }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'weatherscraper.pipelines.WeatherPipeline': 100,

}
DATABASE_URL = os.getenv('PROD_DATABASE_URL')

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


