class Product:
    def __init__(self, order):
        self.order = order
        self.name = None
        self.url = None
        self.seller = None

    def print_items(self):
        print([self.order, self.seller, self.name, self.url])
