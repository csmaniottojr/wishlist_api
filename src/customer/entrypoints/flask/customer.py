from http import HTTPStatus

from flask import jsonify
from flask.views import MethodView

from src.customer.domain import exceptions
from src.customer.domain.services.delete_customer import DeleteCustomer
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


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
