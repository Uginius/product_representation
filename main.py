from htmls.page_getter import OzPageGetter, WbPageGetter


def get_pages():
    wb = WbPageGetter()
    oz = OzPageGetter()
    wb.start()
    oz.start()
    wb.join()
    oz.join()


if __name__ == '__main__':
    get_pages()
