import marshmallow as ma

from src.customer.domain import entities, exceptions


class CreateCustomer:
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository

    def __call__(self, payload):
        if self.customer_repository.has_customer_with_email(payload.get('email')):
            raise exceptions.CustomerAlreadyRegistered

        customer = entities.Customer(
            id=None, name=payload.get('name'), email=payload.get('email')
        )

        self.customer_repository.save(customer)

        return CreateCustomerResponse().dump(customer)


class CreateCustomerRequest(ma.Schema):
    name = ma.fields.String()
    email = ma.fields.Email()


class CreateCustomerResponse(ma.Schema):
    id = ma.fields.Integer()
    name = ma.fields.String()
    email = ma.fields.Email()
