import logging

from flask import Flask

from src.customer.entrypoints.flask import customer, customer_wishlist, customers
from src.orm import start_mappers


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True

    start_mappers()

    register_urls(app)

    app.register_error_handler(Exception, handle_exception)

    return app


def register_urls(app):
    url_view_cls = (
        ('/customers', customers.CustomersView),
        ('/customers/<int:id>', customer.CustomerView),
        (
            '/customers/<int:customer_id>/wishlist/<string:product_id>',
            customer_wishlist.CustomerWishlistView,
        ),
    )
    for url, view_cls in url_view_cls:
        register_url(app, url, view_cls)


def register_url(app, url, view_cls):
    app.add_url_rule(url, view_func=view_cls.as_view(view_cls.__name__))


def handle_exception(exception):
    logging.exception(exception)
