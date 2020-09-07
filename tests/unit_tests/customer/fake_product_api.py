class FakeProductAPI:
    def __init__(self, products_ids):
        self.products_ids = products_ids

    def exists_product_with_id(self, product_id):
        return product_id in self.products_ids
