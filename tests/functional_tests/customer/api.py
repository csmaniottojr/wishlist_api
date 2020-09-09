from tests.functional_tests.wishlist_api import make_api_call


def create_customer(payload, jwt=None):
    return make_api_call('POST', 'customers', payload=payload, jwt=jwt)


def create_customer_returning_id(name, email, jwt):
    payload = {'name': name, 'email': email}
    return create_customer(payload, jwt).json()['id']


def delete_customer(customer_id, jwt=None):
    return make_api_call('DELETE', f'customers/{customer_id}', jwt=jwt)


def list_customers(jwt=None):
    return make_api_call('GET', 'customers', jwt=jwt)


def add_product_to_wishlist(customer_id, product_id, jwt=None):
    wish_list_path = f'customers/{customer_id}/wishlist/{product_id}'
    return make_api_call('POST', wish_list_path, jwt=jwt)


def remove_product_from_wishlist(customer_id, product_id, jwt=None):
    wish_list_path = f'customers/{customer_id}/wishlist/{product_id}'
    return make_api_call('DELETE', wish_list_path, jwt=jwt)


def get_customer(customer_id, jwt=None):
    return make_api_call('GET', f'/customers/{customer_id}', jwt=jwt)


def update_customer(customer_id, payload, jwt=None):
    return make_api_call('PUT', f'/customers/{customer_id}', payload=payload, jwt=jwt)
