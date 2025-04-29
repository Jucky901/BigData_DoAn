import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["ubereats.com"]
    start_urls = ["https://www.ubereats.com/store/baya-bar-west-broadway/BMG311k8XLOVo3CPFSRSaQ?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk5ldyUyMFlvcmslMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJDaElKT3dnXzA2VlB3b2tSWXY1MzRRYVBDOGclMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyZ29vZ2xlX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBNDAuNzEyNzc1MyUyQyUyMmxvbmdpdHVkZSUyMiUzQS03NC4wMDU5NzI4JTdE"]

    def start_requests(self):
        url = "https://www.ubereats.com/store/baya-bar-west-broadway/BMG311k8XLOVo3CPFSRSaQ?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk5ldyUyMFlvcmslMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJDaElKT3dnXzA2VlB3b2tSWXY1MzRRYVBDOGclMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyZ29vZ2xlX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBNDAuNzEyNzc1MyUyQyUyMmxvbmdpdHVkZSUyMiUzQS03NC4wMDU5NzI4JTdE"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid^="store-loaded"]')),
            wait_time=10,
        )
    def parse(self, response):
        tenquan = response.xpath('//*[@id="main-content"]/div/div[1]/div/div[3]/div/div/div[1]/h1/text()').get()
        diachi = response.xpath('//*[@id="main-content"]/div/div[1]/div/div[3]/div/div/div[1]/div/p[2]/span/text()').get()

        items = response.xpath('//*[@id="main-content"]/div/div[7]/div/div/div/div/ul/li/div/ul/li/div/a/div/div/div/div[1]/span/text()').getall()
        prices = response.xpath('//*[@id="main-content"]/div/div[7]/div/div/div/div/ul/li/div/ul/li/div/a/div/div/div/div[2]/span[1]/text()').getall()

        # Ensure the length of items and prices are the same
        for i in range(len(items)):
            yield {
                'tenquan': tenquan,
                'diachi': diachi,
                'item': items[i],
                'price': prices[i]
            }

