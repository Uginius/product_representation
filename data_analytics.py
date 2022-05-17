import json
import re
from openpyxl import Workbook
from src.oz_terms import oz_terms
from src.wb_terms import wb_terms
from utilites import get_last_filename


class DataAnalytics:
    def __init__(self):
        self.json_filename = {'Ozon': get_last_filename('oz'), 'Wildberries': get_last_filename('wb')}
        self.platform_requests = {}
        self.date = {}
        self.rosel_goods = {}
        self.workbook = Workbook()

    def run(self):
        self.initiate_workbook()
        # self.platform_actions(self.workbook.sheetnames[0])
        self.platform_actions(self.workbook.sheetnames[1])
        self.workbook.save(f'xls_result/result_{self.date["Wildberries"]}.xlsx')

    def platform_actions(self, platform):
        self.read_requests(platform)
        self.get_json(platform)
        self.add_titles(platform)
        self.add_body()

    def get_json(self, platform):
        filename = 'result/' + self.json_filename[platform]
        self.date[platform] = re.findall(r'\d{2}-\d{2}-202\d', self.json_filename[platform])[0]
        sellers = ['РОСЭЛ', 'Фотон', 'Safeline', 'Контакт', 'КОНТАКТ Дом', 'Рекорд']
        with open(filename, 'r', encoding='utf8') as file:
            self.rosel_goods = {}
            for line in file:
                json_req = json.loads(line)
                req_id = list(json_req)[0]
                req = list(json_req.values())[0]
                products = [{order: prod['product']} for order, prod in req.items() if prod['seller'] in sellers]
                sls = [prod['seller'] for order, prod in req.items()]
                print(self.platform_requests[req_id], sls)
                self.rosel_goods[req_id] = products
        # pprint(self.rosel_goods)

    def read_requests(self, platform):
        terms = oz_terms if platform == 'Ozon' else wb_terms
        self.platform_requests = {}
        for cat_id, rq in terms.items():
            self.platform_requests.update(rq)

    def add_titles(self, platform):
        titles = ['Целевой запрос', self.date[platform], 'Цель', 'Наименование']
        self.workbook[platform].append(titles)

    def add_body(self):
        for req_id in self.rosel_goods:
            rq = self.platform_requests[req_id]
            rq_goods = self.rosel_goods[req_id]
            target = ''
            result = [rq, len(rq_goods), target, rq_goods]
            print(result)

    def initiate_workbook(self):
        for shop in ['Ozon', 'Wildberries']:
            self.workbook.create_sheet(shop)
        if 'Sheet' in self.workbook.sheetnames:
            self.workbook.remove(self.workbook['Sheet'])


res = DataAnalytics()
res.run()
