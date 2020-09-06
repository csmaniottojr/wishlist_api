from src.customer.domain import exceptions


class DeleteCustomer:
    def __init__(self, customer_repository):
        self.customer_repository = customer_repository

    def __call__(self, payload):
        customer = self.customer_repository.get_by_id(payload.get('customer_id'))
        if not customer:
            raise exceptions.CustomerNotFound

        self.customer_repository.delete(customer)
