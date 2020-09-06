from src.customer.domain.entities import Customer
from src.customer.repository import SQLACustomerRepository


def test_get_by_id(sqla_memory_session):
    customer1 = Customer(id=1, name='Alice', email='alice@gmail.com')
    customer2 = Customer(id=2, name='Bob', email='bob@gmail.com')

    repo = SQLACustomerRepository(sqla_memory_session)
    repo.save(customer1)
    repo.save(customer2)

    assert customer1 == repo.get_by_email('alice@gmail.com')
    assert customer2 == repo.get_by_email('bob@gmail.com')


def test_has_customer_with_email(sqla_memory_session):
    customer1 = Customer(id=1, name='Alice', email='alice@gmail.com')
    customer2 = Customer(id=2, name='Bob', email='bob@gmail.com')

    repo = SQLACustomerRepository(sqla_memory_session)
    repo.save(customer1)
    repo.save(customer2)

    assert repo.has_customer_with_email('alice@gmail.com')
    assert not repo.has_customer_with_email('otheralice@gmail.com')
