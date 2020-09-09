class FakeCustomerRepository:
    def __init__(self):
        self.customers = []

    def get_by_id(self, customer_id):
        return next(
            (customer for customer in self.customers if customer.id == customer_id),
            None,
        )

    def get_by_email(self, email):
        return next(
            (customer for customer in self.customers if customer.email == email), None
        )

    def has_customer_with_email(self, email, customer_id=None):
        if customer_id:
            return any(
                customer
                for customer in self.customers
                if customer.email == email and customer.id != customer_id
            )
        return any(customer for customer in self.customers if customer.email == email)

    def save(self, customer):
        self.customers = [other for other in self.customers if other.id != customer.id]
        self.customers.append(customer)

    def delete(self, customer):
        self.customers.remove(customer)
