from flask import jsonify, request
from flask.views import MethodView

from src.customer.domain import exceptions
from src.customer.domain.services.create_customer import CreateCustomer
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


class CustomersView(MethodView):
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
