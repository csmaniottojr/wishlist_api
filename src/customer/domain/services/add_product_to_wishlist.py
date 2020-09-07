from src.customer.domain import exceptions


class AddProductToWishlist:
    def __init__(self, customer_repository, product_api):
        self.customer_repository = customer_repository
        self.product_api = product_api

    def __call__(self, payload):
        product_id = payload.get('product_id')
        self._check_if_product_exists(product_id)
        customer = self.customer_repository.get_by_id(payload.get('customer_id'))
        customer.add_to_wishlist(product_id)
        self.customer_repository.save(customer)
        return {
            'wishlist': [
                wished_product.product_id for wished_product in customer.wishlist
            ]
        }

    def _check_if_product_exists(self, product_id):
        if not self.product_api.exists_product_with_id(product_id):
            raise exceptions.ProductNotFound
