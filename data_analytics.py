import json
import re
from openpyxl import Workbook
from openpyxl.styles import Font, Side, Border, PatternFill, Alignment
from src.oz_terms import oz_terms, oz_categories
from src.wb_terms import wb_terms, wb_categories
from utilites import get_last_filename

goals =oz_goals
class ProductToXls:
    def __init__(self, prod_id, order, name):
        self.id = int(prod_id)
        self.order = int(order)
        self.name = name

    def data_out(self):
        return {self.id: [self.order, self.name]}

    def order_name(self):
        return f'№{self.order}: {self.name}'


class DataAnalytics:
    def __init__(self):
        self.json_filename = {'Ozon': get_last_filename('oz'), 'Wildberries': get_last_filename('wb')}
        self.platform_requests = {}
        self.first_rq_in_category = {}
        self.categories = {}
        self.date = {}
        self.rosel_goods = {}
        self.workbook = Workbook()
        self.shop = None

    def run(self):
        self.initiate_workbook()
        self.platform_actions(self.workbook.sheetnames[0])
        self.platform_actions(self.workbook.sheetnames[1])
        self.table_footer()
        self.workbook.save(f'xls_result/result_{self.date["Wildberries"]}.xlsx')

    def platform_actions(self, platform):
        self.shop = platform
        self.read_requests()
        self.get_json()
        self.add_caption()
        self.add_titles()
        self.add_body()

    def get_json(self):
        filename = 'result/' + self.json_filename[self.shop]
        self.date[self.shop] = re.findall(r'\d{2}-\d{2}-202\d', self.json_filename[self.shop])[0]
        with open(filename, 'r', encoding='utf8') as file:
            self.rosel_goods = {}
            self.set_rosel_goods(file)

    def set_rosel_goods(self, file):
        sellers = ['РОСЭЛ', 'Фотон', 'Safeline', 'Контакт', 'КОНТАКТ Дом', 'Рекорд', 'ORGANIDE']
        for line in file:
            json_req = json.loads(line)
            req, req_id = list(json_req.values())[0], list(json_req)[0]
            products = [ProductToXls(p['product'], n, p['name']) for n, p in req.items() if p['seller'] in sellers]
            self.rosel_goods[req_id] = products
            # все бренды на 1-й странице
            # sls = [p['seller'] for n, p in req.items()]
            # print(self.platform_requests[req_id], sorted(set(sls)))

    def read_requests(self):
        terms, categories = [oz_terms, oz_categories] if self.shop == 'Ozon' else [wb_terms, wb_categories]
        self.platform_requests = {}
        self.first_rq_in_category = {}
        for cat_id, rq in terms.items():
            self.first_rq_in_category.update({list(rq)[0]: categories[cat_id]})
            self.platform_requests.update(rq)

    def add_caption(self):
        first_line = ['Отчет о представленности продукции по запросам на маркет-плейсах']
        second_line = ['Регион для которого осуществляется поисковая выдача - Москва.']
        sheet = self.workbook[self.shop]
        sheet.append(first_line)
        sheet.append([])
        sheet.append(second_line)
        sheet.append([])
        sheet['A1'].font = Font(name='Calibri', size=20, color="000000", bold=True)
        sheet.row_dimensions[1].height = 40
        sheet.column_dimensions['A'].width = 30
        sheet.column_dimensions['B'].width = 30

    def add_titles(self):
        date = self.date[self.shop].replace('-', '.')
        titles = ['Целевой запрос', 'Цель', date, 'Наименование']
        sheet = self.workbook[self.shop]
        sheet.append(titles)
        thick = Side(border_style="thick", color="000000")
        date_cell = sheet[f'C{sheet.max_row}']
        date_cell.border = Border(top=thick, left=thick, right=thick, bottom=thick)
        col_date = sheet.column_dimensions['C']
        col_goods = sheet.column_dimensions['D']
        col_date.width = 10
        col_goods.width = 40
        col_date.alignment = Alignment(horizontal='center')

    def add_body(self):
        platform = self.shop
        ws = self.workbook[platform]
        for req_id in self.rosel_goods:
            self.check_category(req_id)
            rq = self.platform_requests[req_id]
            condition = ''
            goods = self.rosel_goods[req_id]
            rq_goods = '\n'.join([prod.order_name() for prod in goods])
            result = [rq, condition, len(goods), str(rq_goods)]
            ws.append(result)
            # print(result)

    def check_category(self, req_id):
        if req_id not in self.first_rq_in_category.keys():
            return
        category_name = [self.first_rq_in_category[req_id]]
        sheet = self.workbook[self.shop]
        sheet.append(category_name)
        max_row = sheet.max_row
        sheet.merge_cells(f'A{max_row}:D{max_row}')
        self.set_style_to_categoy_cell(sheet, max_row)

    def initiate_workbook(self):
        for shop in ['Ozon', 'Wildberries']:
            self.workbook.create_sheet(shop)
        if 'Sheet' in self.workbook.sheetnames:
            self.workbook.remove(self.workbook['Sheet'])

    def table_footer(self):
        ws = self.workbook.active
        # ws['A1'].hyperlink = "http://www.google.com"

    def set_style_to_categoy_cell(self, sheet, row_order):
        cat_font = Font(name='Calibri', size=11, color="000000", bold=True)
        thin = Side(border_style="thin", color="000000")
        category_cell = sheet[f'A{row_order}']
        category_cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
        category_cell.fill = PatternFill("solid", fgColor="a6a6a6")
        category_cell.font = cat_font
        rd = sheet.row_dimensions[row_order]
        rd.height = 15


res = DataAnalytics()
res.run()
