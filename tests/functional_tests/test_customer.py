import requests

from src.config import get_api_url


def test_create_customer_returns_status_created():
    payload = {
        'name': 'Cesar Smaniotto Jr',
        'email': 'cesarsjb@gmail.com',
    }

    response = requests.post(f'{get_api_url()}/customers', json=payload)

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

    requests.post(f'{get_api_url()}/customers', json=payload)

    payload = {
        'name': 'Alice',
        'email': email,
    }

    response = requests.post(f'{get_api_url()}/customers', json=payload)
    expected_response = {
        'code': 'CUSTOMER_ALREADY_REGISTERED',
        'message': f'Already exists a customer registered with email {email}',
    }

    assert response.status_code == 422
    assert response.json() == expected_response


def test_delete_customer():
    payload = {
        'name': 'Bob',
        'email': 'bob@gmail.com',
    }

    response = requests.post(f'{get_api_url()}/customers', json=payload)
    customer_id = response.json()['id']

    response = requests.delete(f'{get_api_url()}/customers/{customer_id}')

    assert response.status_code == 204
    assert response.text == ''


def test_delete_inexistent_customer():
    payload = {
        'name': 'Eric',
        'email': 'eric@gmail.com',
    }

    response = requests.post(f'{get_api_url()}/customers', json=payload)
    customer_id = response.json()['id']

    requests.delete(f'{get_api_url()}/customers/{customer_id}')
    response = requests.delete(f'{get_api_url()}/customers/{customer_id}')

    assert response.status_code == 404
    expected_response = {
        'code': 'CUSTOMER_NOT_FOUND',
        'message': f'Customer with id {customer_id} not found',
    }
    assert response.json() == expected_response


def test_list_customers_returns_ok():
    payload = {
        'name': 'Marta',
        'email': 'marta@gmail.com',
    }

    response = requests.post(f'{get_api_url()}/customers', json=payload)

    customer_id = response.json()['id']

    response = requests.get(f'{get_api_url()}/customers')
    expec_customer_in_list = {
        'id': customer_id,
        'name': 'Marta',
        'email': 'marta@gmail.com',
    }

    assert response.status_code == 200
    assert expec_customer_in_list in response.json()
