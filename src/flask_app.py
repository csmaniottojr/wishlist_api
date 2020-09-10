import logging

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager

from src.auth import flask_views as auth_views
from src.config import JWT_SECRET_KEY
from src.customer.entrypoints.flask import customer, customer_wishlist, customers
from src.orm import start_mappers


def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    JWTManager(app)

    app.config.update(
        {
            'APISPEC_SPEC': APISpec(
                title='Wishlist API',
                version='v1',
                plugins=[MarshmallowPlugin()],
                openapi_version='2.0.0',
                info={
                    'description': 'REST API to manage customers and their wishlists.'
                },
                securityDefinitions={
                    'JWT': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}
                },
            ),
            'APISPEC_SWAGGER_URL': '/swagger/',
        }
    )
    docs = FlaskApiSpec(app)

    start_mappers()

    register_urls(app, docs)

    app.register_error_handler(Exception, handle_exception)

    return app


def register_urls(app, docs):
    url_view_cls = (
        ('/customers', customers.CustomersView),
        ('/customers/<int:id>', customer.CustomerView),
        (
            '/customers/<int:customer_id>/wishlist/<string:product_id>',
            customer_wishlist.CustomerWishlistView,
        ),
        ('/auth/signup', auth_views.SignUpView),
        ('/auth/login', auth_views.LoginView),
    )
    for url, view_cls in url_view_cls:
        register_url(app, docs, url, view_cls)


def register_url(app, docs, url, view_cls):
    app.add_url_rule(url, view_func=view_cls.as_view(view_cls.__name__))
    docs.register(view_cls, view_cls.__name__)


def handle_exception(exception):
    logging.exception(exception)
