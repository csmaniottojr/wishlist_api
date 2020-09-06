from flask import jsonify, request
from flask.views import MethodView

from src.customer.domain import exceptions
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
            return jsonify(error), 422
        return jsonify(response._asdict()), 201


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
            return jsonify(error), 404
        return jsonify({}), 204
