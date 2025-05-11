import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

class QuananSpider(scrapy.Spider):
    name = "quanan"
    allowed_domains = ["shopeefood.vn"]
    start_urls = ["https://shopeefood.vn/ho-chi-minh/food/deals"]
    max_page = 10
    id = 1

    def start_requests(self):
        url = "https://shopeefood.vn/ho-chi-minh/food/deals"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_until=EC.presence_of_element_located((By.CLASS_NAME, "item-restaurant")),
            wait_time=10,
        ) 

    def parse(self, response):
        all_href = response.css("div.item-restaurant > a::attr(href)").getall()
        driver = response.meta.get("driver")
        
        for i in range(2, self.max_page + 1):
            next_button = driver.find_element("css selector", "ul.pagination > li:nth-child(12)")  # Check this selector!
            driver.execute_script("arguments[0].click();", next_button)
            
            try:
                time.sleep(10)
                html = driver.page_source
                new_response = Selector(text=html)
                current_href = new_response.css("div.item-restaurant > a::attr(href)").getall()
                all_href += current_href 
            except TimeoutException:
                self.logger.warning("Timed out waiting for div.now-list-restaurant to appear")
                break 

        for i in all_href:
            yield SeleniumRequest(
                url= response.urljoin(i),
                callback= self.parse_chitiet,
                wait_until=EC.presence_of_element_located((By.CLASS_NAME, "item-restaurant-name")),
                wait_time=30
            )
            
    def parse_chitiet(self, response):
        id = self.id

        self.id +=1
        tenquan = response.css("h1.name-restaurant::text").get()
        diachi = response.css("div.address-restaurant::text").get()
        stars = response.css("div.stars > span").getall()
        score = 0

        for star_html in stars:
            sel = Selector(text=star_html)
            class_name = sel.css("span::attr(class)").get()

            if class_name == "full":
                score += 1
            elif class_name == "half":
                score += 0.5
            elif class_name == "empty":
                score += 0
        
        yield{
            'id' : id,
            'tenquan' : tenquan,
            'diachi' : diachi,
            'rating' : score,
        }
