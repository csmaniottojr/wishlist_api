import marshmallow as ma
from sqlalchemy import select

from src.orm import customer as customer_table, wished_product as wished_product_table


class GetCustomerResponse(ma.Schema):
    id = ma.fields.Integer()
    name = ma.fields.String()
    email = ma.fields.Email()
    wishlist = ma.fields.List(ma.fields.UUID())


def get_customer(sqla_session, customer_id):
    customer_stmt = select([customer_table]).where(customer_table.c.id == customer_id)
    customer = sqla_session.execute(customer_stmt).fetchone()

    if not customer:
        return None

    wished_products_stmt = select([wished_product_table.c.product_id]).where(
        wished_product_table.c.customer_id == customer_id
    )
    wished_products = sqla_session.execute(wished_products_stmt).fetchall()

    customer_details = dict(customer)
    customer_details['wishlist'] = [wp.product_id for wp in wished_products]
    return GetCustomerResponse().dump(customer_details)
