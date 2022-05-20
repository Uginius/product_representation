class ProductToXls:
    def __init__(self, prod_id, order, name):
        self.id = int(prod_id)
        self.order = int(order)
        self.name = name

    def data_out(self):
        return {self.id: [self.order, self.name]}

    def order_name(self):
        return f'id:{self.id}, №{self.order}: {self.name}'