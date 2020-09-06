import pytest

from src.customer.domain import exceptions
from src.customer.domain.services.create_customer import (
    CreateCustomer,
    CreateCustomerResponse,
)
from tests.unit_tests.customer.fake_repository import FakeCustomerRepository


def test_customer_saved_in_repository_after_create():
    repo = FakeCustomerRepository()
    service = CreateCustomer(repo)
    payload = {
        'name': 'Cesar Smaniotto Júnior',
        'email': 'cesarsjb@gmail.com',
    }

    service(payload)
    assert repo.get_by_email('cesarsjb@gmail.com') is not None


def test_create_customer_response_dto():
    service = CreateCustomer(FakeCustomerRepository())
    payload = {
        'name': 'Cesar Smaniotto Júnior',
        'email': 'cesarsjb@gmail.com',
    }

    response_dto = service(payload)
    expected_dto = CreateCustomerResponse(
        id=None, name='Cesar Smaniotto Júnior', email='cesarsjb@gmail.com'
    )
    assert response_dto == expected_dto


def test_create_customer_with_duplicated_email():
    service = CreateCustomer(FakeCustomerRepository())
    payload = {
        'name': 'Cesar Smaniotto Júnior',
        'email': 'cesarsjb@gmail.com',
    }
    service(payload)

    payload = {
        'name': 'Cesar Smaniotto Júnior',
        'email': 'cesarsjb@gmail.com',
    }
    with pytest.raises(exceptions.CustomerAlreadyRegistered):
        service(payload)
