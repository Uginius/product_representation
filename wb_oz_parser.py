import os
import re

from bs4 import BeautifulSoup

from product import Product


class Parse:
    def __init__(self, directory):
        self.html_path = directory
        self.request_id = None
        self.files = sorted(os.listdir(directory))
        self.soup = None
        self.prod_list = None
        self.html_product = None
        self.product = None

    def run(self):
        for file in self.files:
            self.request_id = re.findall(r'\d{4}', file)[0]
            self.get_soup(file)
            self.parse()
            break

    def get_soup(self, file):
        filename = f'{self.html_path}/{file}'
        print('opening', filename)
        with open(filename, 'r') as read_file:
            src = read_file.read()
            self.soup = BeautifulSoup(src, 'lxml')

    def parse(self):
        self.get_product_list()
        if not self.prod_list:
            return
        for order, self.html_product in enumerate(self.prod_list):
            self.product = Product(order + 1)
            self.get_elements()
            self.product.print_items()

    def get_product_list(self):
        pass

    def get_elements(self):
        pass


class OzParser(Parse):
    def get_product_list(self):
        self.prod_list = self.soup.find(attrs={'data-widget': 'searchResultsV2'}).div.find_all('div', recursive=False)

    def get_elements(self):
        divs = self.html_product.find_all('div', recursive=False)
        link = divs[1].find('a', class_='tile-hover-target')
        self.product.name = link.text.strip()
        self.product.url = 'https://www.ozon.ru' + link['href'].split('/?')[0]
        self.get_seller(divs[2].find_all('div', recursive=False)[-1].find_all('span')[3].text)

    def get_seller(self, seller):
        if 'продавец' in seller:
            self.product.seller = seller.split('продавец ')[1]
            return
        if seller == 'За час курьером Ozon Express':
            self.product.seller = 'Ozon'
            return
        print(f'-{seller}-')


class WbParser(Parse):
    pass
