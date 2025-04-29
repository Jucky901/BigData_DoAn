BOT_NAME = "doan"

SPIDER_MODULES = ["doan.spiders"]
NEWSPIDER_MODULE = "doan.spiders"

# Fake a browser User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Do NOT obey robots.txt if you want to bypass restrictions (optional)
ROBOTSTXT_OBEY = True

# Ensure only 1 request is sent at a time
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

# Delay between requests (increase if needed)
DOWNLOAD_DELAY = 60

# AutoThrottle: adapt based on server response times
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 10
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.1
AUTOTHROTTLE_DEBUG = True  # Logs throttling stats

# Scrapy-Selenium configuration
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = None  # Use webdriver-manager or set manually
SELENIUM_DRIVER_ARGUMENTS = []

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
    # Optional: rotate User-Agent or use proxies below
}

# Avoid being detected as Selenium
# You can add stealth.js or modify navigator.webdriver later if needed

# Feed output encoding
FEED_EXPORT_ENCODING = "utf-8"

# Optional: Retry logic for failures like 429/503
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [429, 503, 500, 502, 504, 408]
