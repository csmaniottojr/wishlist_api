import os


def get_db_url():
    url_args = {
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST'),
        'port': os.environ.get('POSTGRES_PORT'),
        'db': os.environ.get('POSTGRES_DB'),
    }
    return 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(
        **url_args,
    )


def get_api_url():
    api_host = os.environ.get('API_HOST')
    return f'http://{api_host}:5000'


PRODUCT_API_BASE_URL = os.environ.get(
    'PRODUCT_API_BASE_URL', 'http://challenge-api.luizalabs.com'
)

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
