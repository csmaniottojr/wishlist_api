from dataclasses import dataclass, field
from typing import Set

from src.customer.domain import exceptions


@dataclass(unsafe_hash=True)
class WishedProduct:
    product_id: str


@dataclass
class Customer:
    id: int
    name: str
    email: str
    wishlist: Set[WishedProduct] = field(default_factory=set)

    def update(self, update_payload):
        self.name = update_payload.get('name')
        self.email = update_payload.get('email')

    def add_to_wishlist(self, product_id):
        wished_product = WishedProduct(product_id=product_id)
        if wished_product in self.wishlist:
            raise exceptions.ProductAlreadAddedToWishlist
        self.wishlist.add(wished_product)

    def remove_product_from_wishlist(self, product_id):
        wished_product = WishedProduct(product_id=product_id)
        self.wishlist.remove(wished_product)
