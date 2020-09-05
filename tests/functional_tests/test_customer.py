import requests


def test_create_customer():
    payload = {
        'name': 'Cesar Smaniotto Jr',
        'email': 'cesarsjb@gmail.com',
    }

    response = requests.post('http://localhost:5000/customers', data=payload)

    expected_response = {
        'id': 1,
        'name': 'Cesar Smaniotto Jr',
        'email': 'cesarsjb@gmail.com',
    }

    assert response.json() == expected_response
    assert response.status_code == 201
