from src.customer.domain.entities import Customer, WishedProduct
from src.customer.domain.services.remove_product_from_wishlist import (
    RemoveProductFromWishlist,
)
from tests.unit_tests.customer.fake_repository import FakeCustomerRepository


def test_remove_product_from_wishlist_with_success():
    repo = FakeCustomerRepository()
    customer = Customer(
        id=1,
        name='Alice',
        email='alice@gmail.com',
        wishlist={
            WishedProduct('735e774f-0dbd-4656-852f-b0985c321090'),
            WishedProduct('00bd0eb1-0832-476c-8f44-5494a39c96d8'),
        },
    )
    repo.save(customer)

    service = RemoveProductFromWishlist(repo)
    service({'customer_id': 1, 'product_id': '735e774f-0dbd-4656-852f-b0985c321090'})

    customer = repo.get_by_email('alice@gmail.com')
    assert '735e774f-0dbd-4656-852f-b0985c321090' not in {
        wished_product.product_id for wished_product in customer.wishlist
    }


def test_remove_product_from_wishlist_response():
    repo = FakeCustomerRepository()
    customer = Customer(
        id=1,
        name='Alice',
        email='alice@gmail.com',
        wishlist={
            WishedProduct('735e774f-0dbd-4656-852f-b0985c321090'),
            WishedProduct('00bd0eb1-0832-476c-8f44-5494a39c96d8'),
        },
    )
    repo.save(customer)

    service = RemoveProductFromWishlist(repo)
    response = service(
        {'customer_id': 1, 'product_id': '735e774f-0dbd-4656-852f-b0985c321090'}
    )

    assert response == {'wishlist': ['00bd0eb1-0832-476c-8f44-5494a39c96d8']}
