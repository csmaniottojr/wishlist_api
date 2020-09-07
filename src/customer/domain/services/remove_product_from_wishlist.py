class RemoveProductFromWishlist:
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository

    def __call__(self, payload):
        customer = self.customer_repository.get_by_id(payload.get('customer_id'))
        customer.remove_product_from_wishlist(payload.get('product_id'))
        self.customer_repository.save(customer)
        return {
            'wishlist': [
                wished_product.product_id for wished_product in customer.wishlist
            ]
        }
