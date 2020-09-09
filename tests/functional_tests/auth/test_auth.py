from tests.functional_tests.auth import api


def test_signup_with_success():
    response = api.signup('jonas@gmail.com', 'jonas')

    expected_response = {'message': 'User registered with success'}

    assert response.status_code == 201
    assert response.json() == expected_response


def test_signup_with_email_already_registered():
    email = 'monica@gmail.com'
    api.signup(email, 'monica')
    response = api.signup(email, 'monica')

    expected_response = {
        'code': 'EMAIL_ALREADY_REGISTERED',
        'message': f'Email "{email}" already registered',
    }

    assert response.status_code == 422
    assert response.json() == expected_response


def test_signup_with_invalid_email():
    response = api.signup('jonas@gmailcom', 'jonas')

    expected_response = {
        'code': 'VALIDATION_ERROR',
        'errors': {'email': ['Not a valid email address.']},
        'message': 'Validation error',
    }

    assert response.status_code == 422
    assert response.json() == expected_response


def test_login_with_success():
    api.signup('ana@gmail.com', 'ana123')

    response = api.login('ana@gmail.com', 'ana123')

    assert response.status_code == 200
    assert 'token' in response.json()


def test_login_with_invalid_password():
    api.signup('marcia@gmail.com', 'marcia123')

    response = api.login('marcia@gmail.com', 'm@rcia123')
    expected_response = {
        'code': 'AUTHENTICATION_FAILED',
        'message': 'Wrong email or password',
    }

    assert response.status_code == 401
    assert response.json() == expected_response


def test_login_with_inexistent_user():
    response = api.login('usernotregistered@gmail.com', 'user123')

    expected_response = {
        'code': 'AUTHENTICATION_FAILED',
        'message': 'Wrong email or password',
    }

    assert response.status_code == 401
    assert response.json() == expected_response
