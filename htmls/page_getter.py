import datetime
import os
import random
import time
from threading import Thread

from config import selenium_arguments, browser_path
from src.oz_terms import oz_terms
from src.wb_terms import wb_terms
from utilites import write_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class PageGetter(Thread):
    def __init__(self):
        super().__init__()
        self.platform = ''
        self.terms_dict = {}
        self.category_id = None
        self.search_id = None
        self.term = None
        self.search_url = None
        self.date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.html_dir = None
        self.browser = None

    def run(self):
        self.initiate_browser()
        self.check_html_dir()
        self.search_cycle()
        if self.browser:
            self.browser.close()

    def search_cycle(self):
        for cat_id in self.terms_dict:
            self.category_id = cat_id
            for self.search_id in self.terms_dict[cat_id]:
                self.term = self.terms_dict[cat_id][self.search_id]
                self.get_search_page()

    def get_search_page(self):
        url = self.search_url + self.term
        print(f'connecting to {self.platform}, request id: {self.search_id}, searching: {self.term}')
        self.browser.get(url=url)
        self.scroll_down()
        wait_time = random.randint(3, 7)
        time.sleep(wait_time)
        html_data = self.browser.page_source
        filename = f'{self.html_dir}{self.date}_{self.search_id}.html'
        write_html(html_data, filename)

    def initiate_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument(selenium_arguments[0])
        options.add_argument(selenium_arguments[1])
        self.browser = webdriver.Chrome(service=Service(executable_path=browser_path), options=options)

    def check_html_dir(self):
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)

    def scroll_down(self):
        pass


class OzPageGetter(PageGetter):
    def __init__(self):
        super().__init__()
        self.platform = 'oz'
        self.terms_dict = oz_terms
        self.search_url = 'https://www.ozon.ru/search/?text='
        self.html_dir = f'htmls/{self.date}/oz_html_files/'

    def scroll_down(self):
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.browser.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(1)
        while True:
            self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            time.sleep(1)
            if new_height == last_height:
                break
            last_height = new_height


class WbPageGetter(PageGetter):
    def __init__(self):
        super().__init__()
        self.platform = 'wb'
        self.terms_dict = wb_terms
        self.search_url = 'https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search='
        self.html_dir = f'htmls/{self.date}/wb_html_files/'
