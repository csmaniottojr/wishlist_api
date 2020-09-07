from http import HTTPStatus

from flask import jsonify, request
from flask.views import MethodView

from src.customer import product_api
from src.customer.domain import exceptions
from src.customer.domain.services.add_product_to_wishlist import AddProductToWishlist
from src.customer.domain.services.create_customer import CreateCustomer
from src.customer.domain.services.delete_customer import DeleteCustomer
from src.customer.queries.list_customers import list_customers
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


class CustomersView(MethodView):
    def get(self):
        session = session_factory()
        return jsonify(list_customers(session))

    def post(self):
        session = session_factory()
        repository = SQLACustomerRepository(session)
        try:
            response = CreateCustomer(repository)(request.json)
        except exceptions.CustomerAlreadyRegistered:
            email = request.json.get('email')
            error = {
                'code': 'CUSTOMER_ALREADY_REGISTERED',
                'message': f'Already exists a customer registered with email {email}',
            }
            return jsonify(error), HTTPStatus.UNPROCESSABLE_ENTITY
        return jsonify(response._asdict()), HTTPStatus.CREATED


class CustomerView(MethodView):
    def delete(self, id):
        session = session_factory()
        repository = SQLACustomerRepository(session)
        try:
            DeleteCustomer(repository)({'customer_id': id})
        except exceptions.CustomerNotFound:
            error = {
                'code': 'CUSTOMER_NOT_FOUND',
                'message': f'Customer with id {id} not found',
            }
            return jsonify(error), HTTPStatus.NOT_FOUND
        return '', HTTPStatus.NO_CONTENT


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
