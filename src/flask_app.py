from flask import Flask

from src.customer.flask_endpoints import CustomersView
from src.orm import metadata


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.add_url_rule('/customers', view_func=CustomersView.as_view('customers'))
    return app
