from tests.functional_tests.customer import api


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


def test_create_customer_with_invalid_input():
    payload = {
        'name': 'Cesar Smaniotto Jr',
        'email': 'cesarsjb@gmailcom',
    }

    response = api.create_customer(payload)

    response_json = response.json()

    expected_response = {
        'code': 'VALIDATION_ERROR',
        'errors': {'email': ['Not a valid email address.']},
        'message': 'Validation error',
    }

    assert response_json == expected_response
    assert response.status_code == 422


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


def test_remove_product_to_wishlist_returns_no_content():
    customer_id = api.create_customer_returning_id('Ana', 'ana@gmail.com')

    product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
    other_product_id = '6a512e6c-6627-d286-5d18-583558359ab6'

    api.add_product_to_wishlist(customer_id, product_id)
    api.add_product_to_wishlist(customer_id, other_product_id)
    response = api.remove_product_from_wishlist(customer_id, product_id)

    assert response.status_code == 200
    assert product_id not in response.json()['wishlist']
    assert other_product_id in response.json()['wishlist']


def test_get_customer_details():
    customer_id = api.create_customer_returning_id('Eve', 'eve@gmail.com')

    product_id = '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
    other_product_id = '6a512e6c-6627-d286-5d18-583558359ab6'

    api.add_product_to_wishlist(customer_id, product_id)
    api.add_product_to_wishlist(customer_id, other_product_id)

    expected_response = {
        'id': customer_id,
        'name': 'Eve',
        'email': 'eve@gmail.com',
        'wishlist': [
            '1bf0f365-fbdd-4e21-9786-da459d78dd1f',
            '6a512e6c-6627-d286-5d18-583558359ab6',
        ],
    }

    response = api.get_customer(customer_id)

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_details_from_inexistent_customer():
    customer_id = api.create_customer_returning_id('Martin', 'martin@gmail.com')

    api.delete_customer(customer_id)

    expected_response = {
        'code': 'CUSTOMER_NOT_FOUND',
        'message': f'Customer with id {customer_id} not found',
    }

    response = api.get_customer(customer_id)

    assert response.status_code == 404
    assert response.json() == expected_response


def test_update_customer_with_success():
    customer_id = api.create_customer_returning_id('Harry', 'harry@gmail.com')
    response = api.update_customer(
        customer_id, {'name': 'Harry C', 'email': 'harry.c@gmail.com'}
    )

    expected_response = {
        'id': customer_id,
        'name': 'Harry C',
        'email': 'harry.c@gmail.com',
    }

    assert response.status_code == 200
    assert response.json() == expected_response


def test_update_customer_inexistent():
    customer_id = api.create_customer_returning_id('Cris', 'cris@gmail.com')
    api.delete_customer(customer_id)
    response = api.update_customer(
        customer_id, {'name': 'Cristine', 'email': 'cris@gmail.com'}
    )

    expected_response = {
        'code': 'CUSTOMER_NOT_FOUND',
        'message': f'Customer with id {customer_id} not found',
    }

    assert response.status_code == 404
    assert response.json() == expected_response


def test_update_customer_with_email_of_another_customer():
    email = 'paula@gmail.com'
    customer_id = api.create_customer_returning_id('Dana', 'dana@gmail.com')
    api.create_customer_returning_id('Paula', email)

    response = api.update_customer(
        customer_id, {'name': 'Dana', 'email': 'paula@gmail.com'}
    )

    expected_response = {
        'code': 'CUSTOMER_ALREADY_REGISTERED',
        'message': f'Already exists a customer registered with email {email}',
    }

    assert response.status_code == 422
    assert response.json() == expected_response


def test_update_customer_with_invalid_input():
    customer_id = api.create_customer_returning_id('Lucas', 'lucas@gmail.com')

    response = api.update_customer(
        customer_id, {'name': 'Dana', 'email': 'paula@gmailcom'}
    )

    response_json = response.json()

    expected_response = {
        'code': 'VALIDATION_ERROR',
        'errors': {'email': ['Not a valid email address.']},
        'message': 'Validation error',
    }

    assert response_json == expected_response
    assert response.status_code == 422