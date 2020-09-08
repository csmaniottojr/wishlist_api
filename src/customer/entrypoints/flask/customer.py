from http import HTTPStatus

from flask_apispec.views import MethodResource

from src.customer.domain import exceptions
from src.customer.domain.services.delete_customer import DeleteCustomer
from src.customer.queries.get_customer import get_customer
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


class CustomerView(MethodResource):
    def get(self, id):
        session = session_factory()
        return get_customer(session, id)

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
            return error, HTTPStatus.NOT_FOUND
        return '', HTTPStatus.NO_CONTENT
