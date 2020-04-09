import time
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from ProductScraper.const import *
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from contextlib import contextmanager
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.common.exceptions import TimeoutException
from re import compile

@contextmanager
def wait_for_page_load(browser, timeout=10):
    old_page = browser.find_element_by_tag_name('html')
    yield
    try:
        WebDriverWait(browser, timeout).until(
        staleness_of(old_page)
    )
    except TimeoutException:
        print("timeout!")
        exit()


mpn="MNNH2B/A"
driver = webdriver.Firefox(firefox_binary=FirefoxBinary(webdriverpath))#todo: set implicit wait
driver.implicitly_wait(5)
try:
    driver.get(BaseURL)
except WebDriverException:
    try:
        driver.get(BaseURL)
    except:
        exit()
element = driver.find_element_by_xpath('//*[@id="gh-ac"]')
a = element.text
print(a)
element.send_keys(mpn)
button=driver.find_element_by_xpath('//*[@id="gh-btn"]')
button.click()
# WebDriverWait(driver, 5)
# with wait_for_page_load(driver):
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
print(driver.current_url)
print(driver.page_source)
soup = BeautifulSoup(driver.page_source, 'html.parser')
# reg=compile(r"s-item\s+")
items = soup.select("li[class^=s-item] a")
print(len([item.prettify() for item in items]))
print([item.prettify() for item in items])
a= items.text


item_links = [item.get("href") for item in items]
print(len(item_links))
print(item_links)
# print(soup.prettify())
driver.quit()
# for i in range(100):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(5) https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
# http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html