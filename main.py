from htmls.page_getter import OzPageGetter, WbPageGetter


def get_pages():
    wb = WbPageGetter()
    wb.run()
    # oz = OzPageGetter()
    # oz.run()


if __name__ == '__main__':
    get_pages()
