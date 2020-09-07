import requests

from src.config import get_api_url


def create_customer(payload):
    return requests.post(f'{get_api_url()}/customers', json=payload)


def create_customer_returning_id(name, email):
    payload = {'name': name, 'email': email}
    return create_customer(payload).json()['id']


def delete_customer(customer_id):
    return requests.delete(f'{get_api_url()}/customers/{customer_id}')


def list_customers():
    return requests.get(f'{get_api_url()}/customers')


def add_product_to_wishlist(customer_id, product_id):
    wish_list_url = f'{get_api_url()}/customers/{customer_id}/wishlist/{product_id}'
    return requests.post(wish_list_url)


def remove_product_from_wishlist(customer_id, product_id):
    wish_list_url = f'{get_api_url()}/customers/{customer_id}/wishlist/{product_id}'
    return requests.delete(wish_list_url)


def get_customer(customer_id):
    return requests.get(f'{get_api_url()}/customers/{customer_id}')
