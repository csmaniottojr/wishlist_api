import logging

from flask import Flask, jsonify

from src.customer.flask_endpoints import CustomersView, CustomerView, CustomerWithList
from src.orm import metadata


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.add_url_rule('/customers', view_func=CustomersView.as_view('customers'))
    app.add_url_rule('/customers/<int:id>', view_func=CustomerView.as_view('customer'))
    app.add_url_rule(
        '/customers/<int:customer_id>/wish_list/<string:product_id>',
        view_func=CustomerWithList.as_view('customer_wish_list'),
    )
    app.register_error_handler(Exception, handle_exception)
    return app


def handle_exception(exception):
    logging.exception(exception)
