from data_analytics_monthly import MonthlyDataAnalytics
from htmls.page_getter import OzPageGetter, WbPageGetter
from utilites import get_last_dir, time_track
from wb_oz_parser import OzParser, WbParser


@time_track
def get_pages():
    global wb_search, oz_search
    wb, oz = WbPageGetter(), OzPageGetter()
    if wb_search:
        wb.start()
    if oz_search:
        oz.start()
    if wb_search:
        wb.join()
    if oz_search:
        oz.join()


@time_track
def parse_pages():
    actual_dir = 'htmls/' + get_last_dir()
    if oz_search:
        oz_parser = OzParser(f'{actual_dir}/oz_html_files')
        oz_parser.run()
    if wb_search:
        wb_parser = WbParser(f'{actual_dir}/wb_html_files')
        wb_parser.run()


@time_track
def convert_json_ro_tables():
    res = MonthlyDataAnalytics()
    res.run()


if __name__ == '__main__':
    wb_search = True
    oz_search = True
    # get_pages()
    parse_pages()
    convert_json_ro_tables()
