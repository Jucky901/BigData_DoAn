import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

class GrabstoreSpider(scrapy.Spider):
    name = "grabstore"
    allowed_domains = ["food.grab.com"]
    start_urls = ["https://food.grab.com/vn/en/cuisines/khuy%E1%BA%BFn-m%C3%A3i-delivery/305"]
    max_page = 10

    def start_requests(self):
        url = "https://food.grab.com/vn/en/cuisines/khuy%E1%BA%BFn-m%C3%A3i-delivery/305"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
        ) 

    def parse(self, response):
        driver = response.meta['driver']
        SCROLL_PAUSE_TIME = 2

        # Get the initial scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with the last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(5)
        # Extract the data
        response = Selector(text=driver.page_source)
        tenquan = response.css("h2.name___2epcT::text").getall()
        diachi = "Hà Nội"
        ratings = response.xpath('//*[@id="page-content"]/div[5]/div/div/div[2]/div/div/div/div/a/div/div[2]/div[1]/div[2]/div[1]/text()').getall()
        id = 1

        for i in range(len(tenquan)):
            item = {
                "id" : id,
                "tenquan": tenquan[i],
                "diachi": diachi,
                "rating": ratings[i] if i < len(ratings) else "N/A"
            }
            id += 1
            yield item
