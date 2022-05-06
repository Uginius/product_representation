from htmls.page_getter import OzPageGetter


def get_pages():
    oz = OzPageGetter('qqq')
    oz.run()


if __name__ == '__main__':
    get_pages()
