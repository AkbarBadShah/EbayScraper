from time import sleep
from .const import USER_AGENTS, webdriverpath
from sys import stdout
from datetime import date, datetime
import time
from typing import Tuple, Any
from bs4 import BeautifulSoup
import requests
import logging
import logging.handlers
import os
import random
import re
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver


class Base:

    def __init__(self):
        self.sleep=5
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter(
            "%(asctime)s - %(thread)d - %(levelname)s - %(message)s"
        )
        self.scraper_type = ""
        self.items=[]
        self.comparable_items = {}

    def get_content_simple(self, url: str, default_timeout: int = 10):
        user_agent = random.choice(USER_AGENTS)
        data = requests.get(
            url, headers={"User-Agent": user_agent}, timeout=default_timeout
        )
        return data
        # pickle.dump(data, file)

    @staticmethod
    def log(data):
        file = open(f"{os.getcwd()}/{datetime.now()}.html", 'w')
        print(data)
        file.write(data)

    def link_requestor(self, url: str):
        self.logger.info(f"Querying {url}")
        page = None
        status = False
        error = ""
        try:
            page = self.get_content_simple(url)
        except (
            requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL,
        ):
            error = "Invalid url"
        except (
            requests.exceptions.SSLError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
        ):
            error = "Either we are blocked by the server or internet is unstable!"
            sleep(self.sleep)
            try:
                self.logger.warning("Retrying")
                page = self.get_content_simple(url, default_timeout=60)
            except:
                error = "Its taking tooooooooooooooooooooo long to reconnect!"
            # finally:
            #     return page, error
        except Exception as e:
            self.logger.critical(e)
            error = "Unknown exception!"
        finally:
            if error:
                self.logger.error(f"{error} against {url}")
            else:
                page = BeautifulSoup(page.text, "html.parser")
                status = True

        return page, status

    def log_setup(self):
        self.logger.setLevel(logging.INFO)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        file_name = f"{os.path.dirname(os.path.realpath(__file__))}/logs/{self.scraper_type}/{datetime.now()}"
        handler = logging.handlers.TimedRotatingFileHandler(file_name, when="midnight")
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
        handler = logging.StreamHandler(stdout)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def product_iterator(self, url):
        soup, status = self.link_requestor(url)
        if not status:
            self.logger.info(f"product not found!")
            return status
        else:
            mpn = soup.find("h2", attrs={"itemprop": "mpn"})
            if not mpn:
                mpn = soup.find("div", text="MPN")
                mpn = mpn.findNext("div") if mpn else False
                if mpn:
                    mpn = mpn.get_text()
                    if mpn.find(" ") == -1:  # todo fake check
                        print(mpn)
                        title = soup.find("h1")
                        title = title.get_text() if title else False
                        brand = soup.find("h2", attrs={"itemprop": "brand"})
                        if not brand:
                            brand = soup.find("div", text="Brand")
                            brand = brand.findNext("div") if brand else False
                            brand = brand.get_text() if brand else False
                            item = {'title':title, 'mpn':mpn,'brand':brand}
                            self.items.append(item)
                            self.logger.info(f"Found {item}")
                            return status
                    else:
                        print(mpn)  # todo: remove line after r &D
        self.logger.info("product without MPN, rejected!")
        return status

