import requests

from src.config import get_api_url


def signup(email, password):
    return requests.post(
        f'{get_api_url()}/auth/signup', json={'email': email, 'password': password}
    )


def login(email, password):
    return requests.post(
        f'{get_api_url()}/auth/login', json={'email': email, 'password': password}
    )
