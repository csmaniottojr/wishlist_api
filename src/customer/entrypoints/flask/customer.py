from http import HTTPStatus

from flask_apispec import doc, marshal_with
from flask_apispec.views import MethodResource

from src.customer.domain import exceptions
from src.customer.domain.services.delete_customer import DeleteCustomer
from src.customer.entrypoints.flask.error_schema import ErrorSchema
from src.customer.entrypoints.flask.response_utils import create_response_error
from src.customer.queries.get_customer import get_customer
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


@doc(tags=['customers'])
class CustomerView(MethodResource):
    def get(self, id):
        session = session_factory()
        return get_customer(session, id)

    @marshal_with('', code=HTTPStatus.NO_CONTENT, apply=False)
    @marshal_with(ErrorSchema, code=HTTPStatus.NOT_FOUND, apply=False)
    def delete(self, id):
        session = session_factory()
        repository = SQLACustomerRepository(session)
        try:
            DeleteCustomer(repository)({'customer_id': id})
        except exceptions.CustomerNotFound:
            return create_response_error(
                code='CUSTOMER_NOT_FOUND',
                message=f'Customer with id {id} not found',
                status_code=HTTPStatus.NOT_FOUND,
            )
        return '', HTTPStatus.NO_CONTENT
