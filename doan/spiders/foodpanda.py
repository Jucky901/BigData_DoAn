import scrapy
import json
import re
import random
import time
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent  # Import the UserAgent class from fake_useragent

class FoodpandaSpider(scrapy.Spider):
    name = "foodpanda"
    allowed_domains = ["foodpanda.co.th"]
    start_urls = ["https://www.foodpanda.co.th/restaurant/d15b/gu-roti-cha-chuk-pridi-banomyong"]
    id = 304

    def start_requests(self):
        ua = UserAgent()  # Create an instance of UserAgent to generate random user agents
        for url in self.start_urls:
            # Add random delay before starting each request
            
            # Set up headers with a random user agent
            headers = {
                'User-Agent': ua.random  # Assign a random user agent
            }

            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                headers=headers  # Add headers to each request
            )

    def parse(self, response):
        # Introduce human-like delay between processing each restaurant

        # Initialize item counter or unique ID
        idquan = self.id
        self.id += 1

        # Extract the rating
        rating = response.css("span.bds-c-rating__label-primary::text").get()[0]

        # Extract the street address from the script content
        script_content = response.css('script[data-testid="restaurant-seo-schema"]::text').get()
        diachi = script_content.split('\n')[8].split(':')[1].strip().replace('"','').strip().replace(',','')

        items = response.css('span[data-testid="menu-product-name"]::text').extract()
        prices = response.css('p[data-testid="menu-product-price"]::text').getall()
        # Clean up prices (remove 'from' and currency symbol)
        cleaned_prices = []
        for price in prices:
            cleaned_price = re.sub(r'from\s?|\s?฿', '', price).strip()
            cleaned_prices.append(cleaned_price)

        items_with_prices = list(zip(items, cleaned_prices))
        for item, price in items_with_prices:
            try:
                yield {
                    'id': idquan,
                    'rating': rating,
                    'item': item,
                    'price': int(price) * 789
                }
            except:
                continue
