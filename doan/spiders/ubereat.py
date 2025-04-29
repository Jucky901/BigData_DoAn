import scrapy
import time
import random
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class UbereatSpider(scrapy.Spider):
    name = "ubereat"
    allowed_domains = ["ubereats.com"]
    start_urls = [
        "https://www.ubereats.com/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk5ldyUyMFlvcmslMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJDaElKT3dnXzA2VlB3b2tSWXY1MzRRYVBDOGclMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyZ29vZ2xlX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBNDAuNzEyNzc1MyUyQyUyMmxvbmdpdHVkZSUyMiUzQS03NC4wMDU5NzI4JTdE&ps=1"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid^="store-card"]')),
                wait_time=10,
                script="Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

    def parse(self, response):
        time.sleep(random.uniform(4, 7))  # Delay to simulate page view

        href_all = response.css('a[data-testid="store-card"]::attr(href)').getall()

        for href in href_all:
            full_url = response.urljoin(href)

            # Sleep before each request
            time.sleep(random.uniform(6, 10))

            yield SeleniumRequest(
                url=full_url,
                callback=self.parse_chitiet,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid^="store-loaded"]')),
                wait_time=10,
                script="Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

    def parse_chitiet(self, response):
        time.sleep(random.uniform(3, 6))

        tenquan = response.css("h1::text").get()
        time.sleep(random.uniform(1, 2))

        diachi = response.xpath('//h1[1]/following-sibling::div[1]//p[last()]/span/text()').get()
        time.sleep(random.uniform(1, 2))

        rating = response.xpath('//h1[1]/following-sibling::div[1]//p[1]/span/text()').get()
        time.sleep(random.uniform(1, 2))

        items = response.xpath('//*[@id="main-content"]/div/div[7]/div/div/div/div/ul/li/div/ul/li/div/a/div/div/div/div[1]/span/text()').getall()
        time.sleep(random.uniform(1, 2))

        prices = response.xpath('//*[@id="main-content"]/div/div[7]/div/div/div/div/ul/li/div/ul/li/div/a/div/div/div/div[2]/span[1]/text()').getall()
        time.sleep(random.uniform(1, 2))

        for i in range(len(items)):
            item = items[i]
            price_raw = prices[i] if i < len(prices) else ""
            price = 25000 if price_raw == "Priced by add-ons" else int(float(price_raw.replace('$', '')) * 25000)

            yield {
                'tenquan': tenquan,
                'diachi': diachi,
                'rating': rating,
                'item': item,
                'price': price
            }
