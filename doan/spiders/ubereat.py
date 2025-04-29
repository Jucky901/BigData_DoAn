import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time


class UbereatSpider(scrapy.Spider):
    name = "ubereat"
    allowed_domains = ["ubereats.com"]
    start_urls = ["https://www.ubereats.com/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk5ldyUyMFlvcmslMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJDaElKT3dnXzA2VlB3b2tSWXY1MzRRYVBDOGclMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyZ29vZ2xlX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBNDAuNzEyNzc1MyUyQyUyMmxvbmdpdHVkZSUyMiUzQS03NC4wMDU5NzI4JTdE&ps=1"]

    def start_requests(self):
        url = "https://www.ubereats.com/feed?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMk5ldyUyMFlvcmslMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJDaElKT3dnXzA2VlB3b2tSWXY1MzRRYVBDOGclMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyZ29vZ2xlX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBNDAuNzEyNzc1MyUyQyUyMmxvbmdpdHVkZSUyMiUzQS03NC4wMDU5NzI4JTdE&ps=1"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid^="store-card"]')),
            wait_time=5,
        )
    
    def parse(self, response):
        time.sleep(3)
        href_all = response.css('a[data-testid="store-card"]::attr(href)').getall()
        for i in range(len(href_all)):
            yield SeleniumRequest(
                url= response.urljoin(href_all[i]),
                callback = self.parse_chitiet,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid^="store-loaded"]')),
                wait_time=5,
            )
    def parse_chitiet(self, response):
        time.sleep(3)
        tenquan = response.css("h1::text").get()
        diachi = response.xpath('//h1[1]/following-sibling::div[1]//p[last()]/span/text()').get()

        rating = response.xpath('//h1[1]/following-sibling::div[1]//p[1]/span/text()').get()

        items = response.xpath('//*[@id="main-content"]/div/div[7]/div/div/div/div/ul/li/div/ul/li/div/a/div/div/div/div[1]/span/text()').getall()
        prices = response.xpath('//*[@id="main-content"]/div/div[7]/div/div/div/div/ul/li/div/ul/li/div/a/div/div/div/div[2]/span[1]/text()').getall()

        for i in range(len(items)):
            yield {
                'tenquan': tenquan,
                'diachi': diachi,
                'rating' : rating,
                'item': items[i],
                'price': "25000" if prices[i] == "Priced by add-ons" else int((float(prices[i].replace('$', ''))*25000))
            }
        # yield{
        #     'tenquan': tenquan,
        #     'diachi': diachi,
        #     'rating' : rating,
        # }
        