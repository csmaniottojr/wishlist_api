from http import HTTPStatus

from flask import request
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from src.customer.domain import exceptions
from src.customer.domain.services.create_customer import (
    CreateCustomer,
    CreateCustomerRequest,
    CreateCustomerResponse,
)
from src.customer.entrypoints.flask.error_schema import ErrorSchema
from src.customer.entrypoints.flask.response_utils import (
    create_response_error,
    create_validation_error,
)
from src.customer.queries.list_customers import ListCustomersResponse, list_customers
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


@doc(tags=['customers_wishlist'], security=[{'JWT': []}])
class CustomersView(MethodResource):
    @marshal_with(ListCustomersResponse(many=True), code=HTTPStatus.OK, apply=False)
    @jwt_required
    def get(self):
        session = session_factory()
        return list_customers(session)

    @use_kwargs(CreateCustomerRequest, apply=False)
    @marshal_with(CreateCustomerResponse, HTTPStatus.CREATED, apply=False)
    @marshal_with(ErrorSchema, HTTPStatus.UNPROCESSABLE_ENTITY, apply=False)
    @jwt_required
    def post(self):
        try:
            request_data = CreateCustomerRequest().load(request.json)
        except ValidationError as err:
            return create_validation_error(err)

        session = session_factory()
        repository = SQLACustomerRepository(session)
        try:
            response = CreateCustomer(repository)(request_data)
        except exceptions.CustomerAlreadyRegistered:
            email = request.json.get('email')
            return create_response_error(
                code='CUSTOMER_ALREADY_REGISTERED',
                message=f'Already exists a customer registered with email {email}',
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        return response, HTTPStatus.CREATED
