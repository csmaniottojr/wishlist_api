import requests

from src.config import get_api_url


def make_api_call(method, path, payload=None, jwt=None):
    headers = {}
    if jwt:
        headers['Authorization'] = f'Bearer {jwt}'

    url = f'{get_api_url()}/{path}'
    return requests.request(method, url, json=payload, headers=headers)
