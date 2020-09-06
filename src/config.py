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
