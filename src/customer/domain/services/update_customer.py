import marshmallow as ma

from src.customer.domain import exceptions


class UpdateCustomerRequestResponse(ma.Schema):
    id = ma.fields.Integer()
    name = ma.fields.String()
    email = ma.fields.Email()


class UpdateCustomer:
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository

    def __call__(self, payload):
        email_is_registered = self.customer_repository.has_customer_with_email(
            email=payload.get('email'), customer_id=payload.get('id'),
        )
        if email_is_registered:
            raise exceptions.CustomerAlreadyRegistered

        customer = self.customer_repository.get_by_id(payload.get('id'))
        if not customer:
            raise exceptions.CustomerNotFound

        customer.update(payload)
        response = UpdateCustomerRequestResponse().dump(customer)

        self.customer_repository.save(customer)
        return response
