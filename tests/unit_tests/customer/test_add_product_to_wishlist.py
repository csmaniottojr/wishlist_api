import pytest

from src.customer.domain import entities, exceptions
from src.customer.domain.services.add_product_to_wishlist import AddProductToWishlist
from tests.unit_tests.customer.fake_product_api import FakeProductAPI
from tests.unit_tests.customer.fake_repository import FakeCustomerRepository


def test_add_product_to_wishlist_with_success():
    repo = FakeCustomerRepository()
    product_api = FakeProductAPI(['a33b099f-fe56-46af-901e-7cef5d7ab9c4'])
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))

    service = AddProductToWishlist(repo, product_api)
    service({'customer_id': 1, 'product_id': 'a33b099f-fe56-46af-901e-7cef5d7ab9c4'})

    customer = repo.get_by_email('alice@gmail.com')
    assert 'a33b099f-fe56-46af-901e-7cef5d7ab9c4' in {
        wished_product.product_id for wished_product in customer.wishlist
    }


def test_add_product_to_wishlist_response():
    repo = FakeCustomerRepository()
    product_api = FakeProductAPI(['a33b099f-fe56-46af-901e-7cef5d7ab9c4'])
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))

    service = AddProductToWishlist(repo, product_api)
    response = service(
        {'customer_id': 1, 'product_id': 'a33b099f-fe56-46af-901e-7cef5d7ab9c4'}
    )
    assert response == {'wishlist': ['a33b099f-fe56-46af-901e-7cef5d7ab9c4']}


def test_add_same_product_twice_to_wishlist():
    repo = FakeCustomerRepository()
    product_api = FakeProductAPI(['a33b099f-fe56-46af-901e-7cef5d7ab9c4'])
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))

    service = AddProductToWishlist(repo, product_api)
    service({'customer_id': 1, 'product_id': 'a33b099f-fe56-46af-901e-7cef5d7ab9c4'})

    with pytest.raises(exceptions.ProductAlreadAddedToWishlist):
        service(
            {'customer_id': 1, 'product_id': 'a33b099f-fe56-46af-901e-7cef5d7ab9c4'}
        )


def test_add_inexistent_product_to_wishlist():
    repo = FakeCustomerRepository()
    product_api = FakeProductAPI(['a33b099f-fe56-46af-901e-7cef5d7ab9c4'])
    repo.save(entities.Customer(id=1, name='Alice', email='alice@gmail.com'))

    service = AddProductToWishlist(repo, product_api)

    with pytest.raises(exceptions.ProductNotFound):
        service(
            {'customer_id': 1, 'product_id': 'd6f0530a-f71e-48e8-b3aa-3d71b14cf016'}
        )
