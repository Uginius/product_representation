import datetime
import json
import os
from bs4 import BeautifulSoup
from product import Product
from src.oz_terms import oz_terms
from src.wb_terms import wb_terms


class Parse:
    def __init__(self, directory):
        self.shop = ''
        self.html_path = directory
        self.terms = None
        self.search_terms = {}
        self.request_id = None
        self.files = sorted(os.listdir(directory))
        self.soup = None
        self.prod_list = None
        self.html_product = None
        self.product = None
        self.result_data = {}
        self.empty_block = False

    def run(self):
        self.set_search_terms()
        for file in self.files:
            self.result_data = {}
            self.request_id = file.split('.')[0]
            self.get_soup(file)
            self.parse()
            self.write_json()

    def get_soup(self, file):
        filename = f'{self.html_path}/{file}'
        print(f'opening {filename}, запрос: "{self.search_terms[self.request_id]}"')
        with open(filename, 'r', encoding='utf8') as read_file:
            src = read_file.read()
            self.soup = BeautifulSoup(src, 'lxml')

    def parse(self):
        self.get_product_list()
        if not self.prod_list:
            return
        data = {}
        self.empty_block = False
        for order, self.html_product in enumerate(self.prod_list):
            self.product = Product(order + 1)
            self.get_elements()
            if self.empty_block:
                break
            # self.product.print_items()
            data.update(self.product.data_to_write())
        self.result_data[self.request_id] = data

    def get_product_list(self):
        pass

    def get_elements(self):
        pass

    def set_search_terms(self):
        for el in self.terms:
            self.search_terms.update(self.terms[el])

    def write_json(self):
        filename = f'result/result_{self.shop}_{datetime.datetime.now().strftime("%d-%m-%Y")}.json'
        with open(filename, 'a', encoding='utf8') as write_file:
            data = json.dumps(self.result_data, ensure_ascii=False)
            write_file.write(data)
            write_file.write('\n')


class OzParser(Parse):
    def __init__(self, directory):
        super().__init__(directory)
        self.shop = 'oz'
        self.terms = oz_terms

    def get_product_list(self):
        self.prod_list = self.soup.find(attrs={'data-widget': 'searchResultsV2'}).div.find_all('div', recursive=False)

    def get_elements(self):
        divs = self.html_product.find_all('div', recursive=False)
        try:
            link = divs[1].find('a', class_='tile-hover-target')
        except IndexError:
            self.empty_block = True
            return
        if not link:
            card = divs[0]
            link = card.find('a', class_='tile-hover-target')
            seller_div = card.find_all('div', recursive=False)[-1].find_all('div', recursive=False)[-1]
            self.get_seller(seller_div.find_all(recursive=False)[-1].text)
        else:
            self.get_seller(divs[2].find_all('div', recursive=False)[-1].find_all('span')[3].text)
        self.product.name = link.text.strip()
        self.product.url = 'https://www.ozon.ru' + link['href'].split('/?')[0]
        self.product.id = self.product.url.split('-')[-1]
        # self.product.print_items()

    def get_seller(self, seller):
        if 'продавец' in seller:
            self.product.seller = seller.split('продавец ')[1]
            return
        if seller == 'За час курьером Ozon Express':
            self.product.seller = 'Ozon'
            return


class WbParser(Parse):
    def __init__(self, directory):
        super().__init__(directory)
        self.shop = 'wb'
        self.terms = wb_terms
