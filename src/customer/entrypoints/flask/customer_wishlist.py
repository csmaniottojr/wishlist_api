from http import HTTPStatus

import marshmallow as ma
from flask_apispec import doc, marshal_with
from flask_apispec.views import MethodResource

from src.customer import product_api
from src.customer.domain import exceptions
from src.customer.domain.services.add_product_to_wishlist import AddProductToWishlist
from src.customer.domain.services.remove_product_from_wishlist import (
    RemoveProductFromWishlist,
)
from src.customer.entrypoints.flask.error_schema import ErrorSchema
from src.customer.entrypoints.flask.response_utils import create_response_error
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


class WishlistResponse(ma.Schema):
    wishlist = ma.fields.List(ma.fields.UUID())


@doc(tags=['customers_wishlist'])
class CustomerWishlistView(MethodResource):
    @marshal_with(WishlistResponse, code=HTTPStatus.OK, apply=False)
    @marshal_with(ErrorSchema, code=HTTPStatus.NOT_FOUND, apply=False)
    @marshal_with(ErrorSchema, code=HTTPStatus.UNPROCESSABLE_ENTITY, apply=False)
    def post(self, customer_id, product_id):
        session = session_factory()
        repository = SQLACustomerRepository(session)
        service = AddProductToWishlist(repository, product_api)
        try:
            response = service({'customer_id': customer_id, 'product_id': product_id})
        except exceptions.ProductAlreadAddedToWishlist:
            return create_response_error(
                code='PRODUCT_ALREADY_ADDED',
                message=f'Product with id {product_id} already added to wishlist',
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        except exceptions.ProductNotFound:
            return create_response_error(
                code='PRODUCT_NOT_FOUND',
                message=f'Product with id {product_id} not found',
                status_code=HTTPStatus.NOT_FOUND,
            )

        return response, HTTPStatus.CREATED

    @marshal_with(WishlistResponse, code=HTTPStatus.OK, apply=False)
    def delete(self, product_id, customer_id):
        session = session_factory()
        repository = SQLACustomerRepository(session)
        service = RemoveProductFromWishlist(repository)
        return service({'customer_id': customer_id, 'product_id': product_id})
