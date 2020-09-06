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
