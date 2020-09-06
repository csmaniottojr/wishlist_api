from flask import jsonify, request
from flask.views import MethodView

from src.customer.domain.services.create_customer import CreateCustomer
from src.customer.repository import SQLACustomerRepository
from src.db import session_factory


class CustomersView(MethodView):
    def post(self):
        payload = dict(request.json)
        session = session_factory()
        repository = SQLACustomerRepository(session)
        service = CreateCustomer(repository)
        response = service(payload)
        return jsonify(response._asdict()), 201
