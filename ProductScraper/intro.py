import requests
from bs4 import BeautifulSoup


class EbayWrapper:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/77.0.3865.90 Safari/537.36"
    }

    def __init__(self):
        self.BASE_URL = "https://www.ebay.com/n/all-categories"
        self.all_categories = ["electronics"]

    def get_content(self, url):
        print(f"getting {url}")
        data = requests.get(url, headers=self.headers)
        return data

    def get_parsed_data(self, content):
        return BeautifulSoup(content,"html.parser")

    def get_all_links_in_category(self, category, all_categories):
        supported_category = [cat for cat in all_categories if cat.get('id') == category]
        supported_category = supported_category[0]

        all_sub_categories = list()
        for main_category in supported_category.find_all('ul', attrs={'class': 'sub-cats'}):
            all_sub_categories.extend(main_category.find_all('li'))

        all_sub_categories = [category for category in all_sub_categories if category.get('_sp')]
        all_sub_categories = [category.find('a').get('href') for category in all_sub_categories if
                              'view-more-link' not in category.get('class', [])]
        return all_sub_categories

    def get_page_items(self, link, count):
        html = self.get_content(f"{link}?_pgn={count}")
        soup = self.get_parsed_data(html.text)
        print(soup.prettify())
        items = soup.find_all('li', attrs={'class': 's-item'})
        return items

    def iterate_over_each_item(self, items):
        count=0
        for item in items:
            count+=1
            print("item")
            item_link = item.find('a').get('href')
            html = self.get_content(item_link)
            soup = self.get_parsed_data(html.text)
            item_specifics = soup.find('div', attrs={'class': 'app-itemspecifics-mobile-wrapper'})
            brand, mpn_value = None, None
            price = soup.find('div', attrs={'class': 'main-price-with-shipping'})
            price = price.text
            for attributes in item_specifics.find_all('div', attrs={'class': 'ui-component-map-wrapper'}):
                if brand and mpn_value:
                    break

                if 'Brand' in attributes.text:
                    mpn_value = attributes.find('div', attrs={'class': 'cc-value'}).text.strip()
                if 'MPN' in attributes.text:
                    mpn_value = attributes.find('div', attrs={'class': 'cc-value'}).text.strip()

            print(price, brand, mpn_value)
            if count>1:
                break

    def iterate_over_each_page(self, link):
        next_page = True
        count = 1
        while next_page:
            items = self.get_page_items(link, count)
            print(items)
            if not items:
                next_page = False

            self.iterate_over_each_item(items)
            break

    def iterate_over_each_link(self, all_links):
        for link in all_links:
            self.iterate_over_each_page(link)
            break


    def run(self):
        html = self.get_content(self.BASE_URL)
        soup = self.get_parsed_data(html.text)
        print("dello")
        categories = soup.find_all('div', attrs={'class': 'cat-container'})
        for category in self.all_categories:
            print("dello")
            all_links = self.get_all_links_in_category(category, categories)
            print("dello")
            self.iterate_over_each_link(all_links)
            print("dello")

if __name__ == "__main__":
    status=EbayWrapper().run()
