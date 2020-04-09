from ProductScraper.Base import Base
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from ProductScraper.const import *
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from contextlib import contextmanager
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import TimeoutException

class ProductFinder(Base):

    def __init__(self):
        super().__init__()
        self.scraper_type = "ProductFinderLogs"
        self.log_setup()

    @contextmanager
    def wait_for_page_load(self, browser, timeout=10):
        old_page = browser.find_element_by_tag_name('html')
        yield
        try:
            WebDriverWait(browser, timeout).until(
            staleness_of(old_page)
        )
        except TimeoutException:
            self.logger.info("timeout!")
            exit()

    def get_related_products(self, mpn):
        driver = webdriver.Firefox(firefox_binary=FirefoxBinary(webdriverpath))#todo: set implicit wait
        driver.implicitly_wait(5)
        status = False
        try:
            driver.get(BaseURL)
        except WebDriverException:
            return status

        element = driver.find_element_by_xpath('//*[@id="gh-ac"]')
        element.send_keys(mpn)
        button=driver.find_element_by_xpath('//*[@id="gh-btn"]')
        button.click()
        self.logger.info(driver.current_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select("li[class^=s-item] a[class=s-item__link]")
        item_count= int(soup.find("h1", attrs={'class':'srp-controls__count-heading'}).find('span').get_text())
        self.logger.info(f"Items found: {item_count}")
        items = items[0:item_count]
        # t=[item.prettify() for item in items]Todo: remove after testing
        # self.logger.info(len(t))
        if item_count:
            # for i in t:Todo: remove after testing
            #     self.logger.info(i)
            #     self.logger.info(f'\n\nbreak{ind}')
            #     ind+=1
            items = [item.get("href") for item in items]
            self.logger.info(f"Items links: {items}")
        else:
            self.logger.info("No similar products!")

        driver.quit()
        status = True
        return items, status

    def run(self):
        item="MNNH2B/A"
        items, status = self.get_related_products(item)
        if not status:
            return False
        self.comparable_items[item] = [items]
        return True

if __name__ == "__main__":
    status = ProductFinder().run()
    print(status)

        # for i in range(100):
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(5) https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
        # http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html