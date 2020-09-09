from tests.functional_tests.wishlist_api import make_api_call


def signup(email, password):
    payload = {'email': email, 'password': password}
    return make_api_call('POST', 'auth/signup', payload=payload)


def login(email, password):
    payload = {'email': email, 'password': password}
    return make_api_call('POST', 'auth/login', payload=payload)
