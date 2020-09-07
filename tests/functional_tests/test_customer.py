from tests.functional_tests import api


def test_create_customer_returns_status_created():
    payload = {
        'name': 'Cesar Smaniotto Jr',
        'email': 'cesarsjb@gmail.com',
    }

    response = api.create_customer(payload)

    response_json = response.json()

    expected_response = {
        'name': 'Cesar Smaniotto Jr',
        'email': 'cesarsjb@gmail.com',
    }

    assert 'id' in response_json
    response_json.pop('id')

    assert response_json == expected_response
    assert response.status_code == 201


def test_create_customer_with_duplicated_email():
    email = 'alice@gmail.com'
    payload = {
        'name': 'Alice',
        'email': email,
    }

    api.create_customer(payload)

    payload = {
        'name': 'Alice',
        'email': email,
    }

    response = api.create_customer(payload)
    expected_response = {
        'code': 'CUSTOMER_ALREADY_REGISTERED',
        'message': f'Already exists a customer registered with email {email}',
    }

    assert response.status_code == 422
    assert response.json() == expected_response


def test_delete_customer():
    customer_id = api.create_customer_returning_id('Bob', 'bob@gmail.com')

    response = api.delete_customer(customer_id)

    assert response.status_code == 204
    assert response.text == ''


def test_delete_inexistent_customer():
    customer_id = api.create_customer_returning_id('Eric', 'eric@gmail.com')

    api.delete_customer(customer_id)
    response = api.delete_customer(customer_id)

    assert response.status_code == 404
    expected_response = {
        'code': 'CUSTOMER_NOT_FOUND',
        'message': f'Customer with id {customer_id} not found',
    }
    assert response.json() == expected_response


def test_list_customers_returns_ok():
    customer_id = api.create_customer_returning_id('Marta', 'marta@gmail.com')

    response = api.list_customers()
    expec_customer_in_list = {
        'id': customer_id,
        'name': 'Marta',
        'email': 'marta@gmail.com',
    }

    assert response.status_code == 200
    assert expec_customer_in_list in response.json()


def test_add_product_to_wishlist_returns_created():
    customer_id = api.create_customer_returning_id('John', 'john@gmail.com')

    product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
    other_product_id = '6a512e6c-6627-d286-5d18-583558359ab6'

    api.add_product_to_wishlist(customer_id, product_id)
    response = api.add_product_to_wishlist(customer_id, other_product_id)

    assert response.status_code == 201
    assert product_id in response.json()['wishlist']
    assert other_product_id in response.json()['wishlist']


def test_same_product_cannot_added_twice_to_wishlist():
    customer_id = api.create_customer_returning_id('Mary', 'mary@gmail.com')

    product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'

    api.add_product_to_wishlist(customer_id, product_id)
    response = api.add_product_to_wishlist(customer_id, product_id)

    expected_response = {
        'code': 'PRODUCT_ALREADY_ADDED',
        'message': f'Product with id {product_id} already added to wishlist',
    }

    assert response.status_code == 422
    assert response.json() == expected_response


def test_cannot_add_inexistent_product_to_wishlist():
    customer_id = api.create_customer_returning_id('Joe', 'joe@gmail.com')

    product_id = '5ddbc2b9-1186-4c38-b65e-ce8949ee91b5'

    api.add_product_to_wishlist(customer_id, product_id)
    response = api.add_product_to_wishlist(customer_id, product_id)

    expected_response = {
        'code': 'PRODUCT_NOT_FOUND',
        'message': f'Product with id {product_id} not found',
    }

    assert response.status_code == 404
    assert response.json() == expected_response
