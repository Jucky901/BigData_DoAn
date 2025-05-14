import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

class GrabfoodSpider(scrapy.Spider):
    name = "grabfood"
    allowed_domains = ["food.grab.com"]
    start_urls = ["https://food.grab.com/vn/en/cuisines/khuy%E1%BA%BFn-m%C3%A3i-delivery/305"]
    max_page = 10
    id = 1

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
        new_response = Selector(text=driver.page_source)
        all_hrefs = new_response.css("div.RestaurantListCol___1FZ8V > a::attr(href)").getall()

        for url in all_hrefs:
            yield SeleniumRequest(
            url= response.urljoin(url),
            callback=self.parse_chitiet,
        )
    def parse_chitiet(self, response):
        driver = response.meta["driver"]

        try:
            # Wait for the menu items to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.itemNameTitle___1sFBq"))
            )
            time.sleep(2)  # Simulate a brief human delay

            id = self.id
            self.id += 1

            rating = response.css("div.ratingText___1Q08c::text").get()
            items = response.css("p.itemNameTitle___1sFBq::text").getall()
            prices = response.css("p.discountedPrice___3MBVA::text").getall()

            # Iterating over items
            for i in range(len(items)):
                time.sleep(1)  # Slight delay before each item processing

                yield {
                    'idquan': id,
                    'rating': rating,
                    'items': items[i],
                    'price': prices[i] if i < len(prices) else "N/A"  # Handle missing prices
                }

        except TimeoutException:
            self.logger.warning(f"Timeout while loading menu items for {response.url}")

