import requests

from src.config import get_api_url


def test_create_customer():
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
