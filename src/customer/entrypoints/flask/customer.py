from http import HTTPStatus

from flask import request
from flask_apispec import doc, marshal_with
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.customer.domain import exceptions
from src.customer.domain.services.delete_customer import DeleteCustomer
from src.customer.domain.services.update_customer import (
    UpdateCustomer,
    UpdateCustomerRequestResponse,
)
from src.customer.entrypoints.flask.error_schema import ErrorSchema
from src.customer.entrypoints.flask.response_utils import (
    create_response_error,
    create_validation_error,
)
from src.customer.queries.get_customer import GetCustomerResponse, get_customer
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


@doc(tags=['customers'], security=[{'JWT': []}])
class CustomerView(MethodResource):
    @marshal_with(GetCustomerResponse, code=HTTPStatus.OK, apply=False)
    @marshal_with(ErrorSchema, code=HTTPStatus.NOT_FOUND, apply=False)
    @jwt_required
    def get(self, id):
        session = session_factory()
        customer = get_customer(session, id)
        if customer:
            return customer
        return create_response_error(
            code='CUSTOMER_NOT_FOUND',
            message=f'Customer with id {id} not found',
            status_code=HTTPStatus.NOT_FOUND,
        )

    @marshal_with(UpdateCustomerRequestResponse, code=HTTPStatus.OK, apply=False)
    @marshal_with(ErrorSchema, code=HTTPStatus.NOT_FOUND, apply=False)
    @marshal_with(ErrorSchema, HTTPStatus.UNPROCESSABLE_ENTITY, apply=False)
    @jwt_required
    def put(self, id):
        request_data = {**request.json, 'id': id}
        try:
            request_data = UpdateCustomerRequestResponse().load(request_data)
        except ValidationError as err:
            return create_validation_error(err)

        session = session_factory()
        repository = SQLACustomerRepository(session)
        try:
            response = UpdateCustomer(repository)(request_data)
        except exceptions.CustomerNotFound:
            return create_response_error(
                code='CUSTOMER_NOT_FOUND',
                message=f'Customer with id {id} not found',
                status_code=HTTPStatus.NOT_FOUND,
            )
        except exceptions.CustomerAlreadyRegistered:
            email = request_data.get('email')
            return create_response_error(
                code='CUSTOMER_ALREADY_REGISTERED',
                message=f'Already exists a customer registered with email {email}',
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        return response, HTTPStatus.OK

    @marshal_with('', code=HTTPStatus.NO_CONTENT, apply=False)
    @marshal_with(ErrorSchema, code=HTTPStatus.NOT_FOUND, apply=False)
    @jwt_required
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
