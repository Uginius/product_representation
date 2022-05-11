from htmls.page_getter import OzPageGetter, WbPageGetter
from utilites import get_last_dir
from wb_oz_parser import OzParser, WbParser


def get_pages():
    wb = WbPageGetter()
    oz = OzPageGetter()
    wb.start()
    oz.start()
    wb.join()
    oz.join()


def parse_pages():
    actual_dir = 'htmls/' + get_last_dir()
    oz_parser = OzParser(f'{actual_dir}/oz_html_files')
    oz_parser.run()
    # wb_parser = WbParser(f'{actual_dir}/wb_html_files')
    # wb_parser.run()


if __name__ == '__main__':
    # get_pages()
    parse_pages()
