from collections import namedtuple

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

        return CreateCustomerResponse(
            id=customer.id, name=customer.name, email=customer.email,
        )


CreateCustomerResponse = namedtuple('CreateCustomerResponse', 'id name email')
