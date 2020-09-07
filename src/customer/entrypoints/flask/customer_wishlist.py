from http import HTTPStatus

from flask import jsonify
from flask.views import MethodView

from src.customer import product_api
from src.customer.domain import exceptions
from src.customer.domain.services.add_product_to_wishlist import AddProductToWishlist
from src.customer.domain.services.remove_product_from_wishlist import (
    RemoveProductFromWishlist,
)
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


class CustomerWishlistView(MethodView):
    def post(self, customer_id, product_id):
        session = session_factory()
        repository = SQLACustomerRepository(session)
        service = AddProductToWishlist(repository, product_api)
        try:
            response = service({'customer_id': customer_id, 'product_id': product_id})
        except exceptions.ProductAlreadAddedToWishlist:
            error = {
                'code': 'PRODUCT_ALREADY_ADDED',
                'message': f'Product with id {product_id} already added to wishlist',
            }
            return jsonify(error), HTTPStatus.UNPROCESSABLE_ENTITY
        except exceptions.ProductNotFound:
            error = {
                'code': 'PRODUCT_NOT_FOUND',
                'message': f'Product with id {product_id} not found',
            }
            return jsonify(error), HTTPStatus.NOT_FOUND

        return jsonify(response), HTTPStatus.CREATED

    def delete(self, product_id, customer_id):
        session = session_factory()
        repository = SQLACustomerRepository(session)
        service = RemoveProductFromWishlist(repository)
        return service({'customer_id': customer_id, 'product_id': product_id})
