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


def test_delete_wished_product_when_delete_customer(sqla_memory_session):
    customer = Customer(id=1, name='Alice', email='alice@gmail.com')
    customer.add_to_wishlist('PRODUCT_UUID')

    repo = SQLACustomerRepository(sqla_memory_session)
    repo.save(customer)
    repo.delete(customer)

    assert repo.get_by_id(1) is None

    count_wished = sqla_memory_session.execute(
        'SELECT count(*) FROM wished_product WHERE customer_id = :id', {'id': 1}
    ).scalar()

    assert count_wished == 0
