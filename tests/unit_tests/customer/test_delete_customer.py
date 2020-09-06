import pytest

from src.customer.domain import entities, exceptions
from src.customer.domain.services.delete_customer import DeleteCustomer
from tests.unit_tests.customer.fake_repository import FakeCustomerRepository


def test_delete_customer_with_success():
    repo = FakeCustomerRepository()
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))
    service = DeleteCustomer(repo)
    service({'customer_id': 1})

    assert repo.get_by_email('alice@gmail.com') is None


def test_delete_inexistent_customer():
    repo = FakeCustomerRepository()
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))
    service = DeleteCustomer(repo)

    with pytest.raises(exceptions.CustomerNotFound):
        service({'customer_id': 2})
