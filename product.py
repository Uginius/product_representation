class Product:
    def __init__(self, order):
        self.order = order
        self.name = None
        self.url = None
        self.seller = None
        self.id = None

    def print_items(self):
        print([self.order, self.seller, self.name, self.url])

    def data_to_write(self):
        return {self.order: [self.seller, self.id, self.name, self.url]}
