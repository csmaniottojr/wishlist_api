import marshmallow as ma
from sqlalchemy import select

from src.orm import customer as customer_table


def list_customers(sqla_session):
    customers = sqla_session.execute(select([customer_table])).fetchall()
    return ListCustomersResponse().dump(customers, many=True)


class ListCustomersResponse(ma.Schema):
    id = ma.fields.Integer()
    name = ma.fields.String()
    email = ma.fields.Email()
