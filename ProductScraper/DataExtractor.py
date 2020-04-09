import time
from ProductScraper.Base import Base
from ProductScraper.const import BaseURL
import random


class EbayScraper(Base):
    def __init__(self):
        super().__init__()
        self.scraper_type = "ProductScraperLogs"
        self.log_setup()
        self.choice = random.choice(range(10))#todo: remove

    def get_category(self, url):
        soup, status = self.link_requestor(url)
        if not status:
            return []
        else:
            categories = soup.find_all("div", attrs={"class": "cat-container"})
            category = [
                category
                for category in categories
                if category.get("id") == "electronics"
            ]
            # Todo: return all_categories
            return category[0]

    @staticmethod
    def all_categories(category):
        sub_categories = category.find_all("li")
        sub_categories = [
            category for category in sub_categories if category.get("_sp")
        ]
        sub_categories = [
            category.find("a").get("href")
            for category in sub_categories
            if "view-more-link" not in category.get("class", [])
        ]
        return sub_categories

    def get_sub_category(self, category):
        sub_categories = list()
        for category in category.find_all("ul", attrs={"class": "sub-cats"}):
            sub_categories.extend(self.all_categories(category))
            break
        return sub_categories

    def page_iterator(self, url):
        next_page = True
        count = 1
        item_links = []
        while next_page:
            soup, status = self.link_requestor(f"{url}?_pgn={count}")
            if status:
                items = soup.find_all("li", attrs={"class": "s-item"})
                if not items or count == 2:  # Todo: erase count>2
                    return item_links
                item_links.extend([item.find("a").get("href") for item in items])
                count += 1
            else:
                return item_links
    #
    # def product_iterator(self, url):
    #     soup, error = self.link_requestor(url)
    #     if status
    #     title = soup.find("h1")
    #     title = title.get_text() if title else False
    #     brand = soup.find("h2", attrs={"itemprop": "brand"})
    #     if not brand:
    #         brand = soup.find("div", text="Brand")
    #         brand = brand.findNext("div") if brand else False
    #     brand = brand.get_text() if brand else False
    #     mpn = soup.find("h2", attrs={"itemprop": "mpn"})
    #     if not mpn:
    #         mpn = soup.find("div", text="MPN")
    #         mpn = mpn.findNext("div") if mpn else False
    #     if mpn:
    #         mpn = mpn.get_text()
    #         if mpn.find(" ") == -1:#todo fake check
    #             return title, mpn, brand
    #         else:
    #             print(mpn)  # todo: remove line after r &D
    #     return False

    def run(self):
        # Todo: for multiprocessing
        # pool = ThreadPool(processes=self.THREADS)
        # for l, ul in pool.imap_unordered(self.link_extractor, urls):
        category = self.get_category(BaseURL)
        if not category:
            self.logger.error("No category")
            return False
        self.logger.info(f"Category Found")
        sub_categories = self.get_sub_category(category)
        self.logger.info(sub_categories[3])
        item_list = self.page_iterator(
            sub_categories[3]
        )  # todo: insert loop [no index]
        # self.logger.info(item_list)
        if not item_list:
            self.logger.info("no item on the page!")
            return False
        count = 1
        for item in item_list:
            status = self.product_iterator(item)
            self.logger.info(status)
            if not status:
                continue
            count += 1
            if count > 10:
                break
            time.sleep(5)
        return True, self.items


if __name__ == "__main__":
    status, items = EbayScraper().run()
    print(f"{status}\n{items}")
