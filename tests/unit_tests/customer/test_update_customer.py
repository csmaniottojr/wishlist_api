import pytest

from src.customer.domain import entities, exceptions
from src.customer.domain.services.update_customer import UpdateCustomer
from tests.unit_tests.customer.fake_repository import FakeCustomerRepository


def test_update_customer_with_success():
    repo = FakeCustomerRepository()
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))
    service = UpdateCustomer(repo)
    service({'id': 1, 'name': 'Alicia', 'email': 'alicia@gmail.com'})

    customer = repo.get_by_id(1)
    assert customer.name == 'Alicia'
    assert customer.email == 'alicia@gmail.com'


def test_create_customer_response_dto():
    repo = FakeCustomerRepository()
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))
    service = UpdateCustomer(repo)
    response_dto = service({'id': 1, 'name': 'Alicia', 'email': 'alicia@gmail.com'})

    expected_dto = {'id': 1, 'name': 'Alicia', 'email': 'alicia@gmail.com'}
    assert response_dto == expected_dto


def test_update_inexistent_customer():
    repo = FakeCustomerRepository()
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))
    service = UpdateCustomer(repo)

    with pytest.raises(exceptions.CustomerNotFound):
        service({'id': 2, 'name': 'Alicia', 'email': 'alicia@gmail.com'})


def test_update_customer_with_email_of_another_customer():
    repo = FakeCustomerRepository()
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))
    repo.save(entities.Customer(id=2, name='Carla', email='carla@gmail.com'))
    service = UpdateCustomer(repo)

    with pytest.raises(exceptions.CustomerAlreadyRegistered):
        service({'id': 1, 'name': 'Carla', 'email': 'carla@gmail.com'})


def test_update_customer_mantaining_same_email():
    repo = FakeCustomerRepository()
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))
    service = UpdateCustomer(repo)

    service({'id': 1, 'name': 'Alicia', 'email': 'alice@gmail.com'})

    customer = repo.get_by_id(1)
    assert customer.name == 'Alicia'
    assert customer.email == 'alice@gmail.com'
