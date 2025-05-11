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

class FoodpandastoreSpider(scrapy.Spider):
    name = "foodpandastore"
    allowed_domains = ["foodpanda.co.th"]
    start_urls = ["https://www.foodpanda.co.th/restaurant/d15b/gu-roti-cha-chuk-pridi-banomyong"]
    id = 304

    def start_requests(self):
        for url in self.start_urls:
            # Add random delay before starting each request
            time.sleep(random.uniform(2, 5))  # Human-like delay
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
            )

    def parse(self, response):
        # Introduce human-like delay between processing each restaurant
        time.sleep(random.uniform(3, 6))  # Simulate human browsing

        # Initialize item counter or unique ID
        id = self.id
        self.id += 1
        tenquan = response.css("h1.main-info__title::text").get()
        # Extract the rating
        rating = response.css("span.bds-c-rating__label-primary::text").get()[0]

        # Extract the street address from the script content
        script_content = response.css('script[data-testid="restaurant-seo-schema"]::text').get()
        diachi = script_content.split('\n')[8].split(':')[1].strip().replace('"','').strip().replace(',','')

        items = response.css('span[data-testid="menu-product-name"]::text').extract()
        prices = response.css('p[data-testid="menu-product-price"]::text').getall()

        yield{
            'id' : id,
            'tenquan' : tenquan,
            'diachi' : diachi,
            'rating' : rating
        }


        
