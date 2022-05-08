import datetime
import os
import time

import requests
from config import headers
from src.oz_terms import oz_terms
from src.wb_terms import wb_terms
from utilites import write_html


class PageGetter:
    def __init__(self):
        self.platform = ''
        self.terms_dict = {}
        self.category_id = None
        self.search_id = None
        self.term = None
        self.search_url = None
        self.date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.html_dir = None

    def run(self):
        self.check_html_dir()
        self.search_cycle()

    def search_cycle(self):
        for cat_id in self.terms_dict:
            self.category_id = cat_id
            for self.search_id in self.terms_dict[cat_id]:
                self.term = self.terms_dict[cat_id][self.search_id]
                self.get_search_page()
                break
            break

    def get_search_page(self):
        # url = self.search_url + self.term
        url = 'https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=%D1%83%D0%B4%D0%BB%D0%B8%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C'
        print(url)
        r = requests.get(url, headers=headers)
        print(r.status_code)
        time.sleep(2)
        # print(r.text)
        src = r.text
        filename = f'{self.html_dir}{self.search_id}.html'
        write_html(src, filename)

    def check_html_dir(self):
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)


class OzPageGetter(PageGetter):
    def __init__(self):
        super().__init__()
        self.platform = 'oz'
        self.terms_dict = oz_terms
        self.search_url = 'https://www.ozon.ru/search/?text='
        self.html_dir = f'htmls/{self.date}/oz_html_files/'


class WbPageGetter(PageGetter):
    def __init__(self):
        super().__init__()
        self.platform = 'wb'
        self.terms_dict = wb_terms
        self.search_url = 'https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search='
        self.html_dir = f'htmls/{self.date}/wb_html_files/'
