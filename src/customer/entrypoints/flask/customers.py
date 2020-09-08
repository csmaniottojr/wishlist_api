from http import HTTPStatus

from flask import request
from flask_apispec.views import MethodResource

from src.customer.domain import exceptions
from src.customer.domain.services.create_customer import CreateCustomer
from src.customer.queries.list_customers import list_customers
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


class CustomersView(MethodResource):
    def get(self):
        session = session_factory()
        return list_customers(session)

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
            return error, HTTPStatus.UNPROCESSABLE_ENTITY
        return response._asdict(), HTTPStatus.CREATED
