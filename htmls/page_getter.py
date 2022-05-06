class PageGetter:
    def __init__(self, word):
        self.rq_word = word

    def run(self):
        pass


class OzPageGetter(PageGetter):
    def __init__(self, word):
        super().__init__(word)
