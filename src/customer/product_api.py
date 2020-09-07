import requests


def exists_product_with_id(product_id):
    url = f'http://challenge-api.luizalabs.com/api/product/{product_id}/'
    response = requests.get(url)
    return response.status_code == 200
