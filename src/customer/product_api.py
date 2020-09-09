import requests

from src.config import PRODUCT_API_BASE_URL


def exists_product_with_id(product_id):
    url = f'{PRODUCT_API_BASE_URL}/api/product/{product_id}/'
    response = requests.get(url)
    return response.status_code == 200
