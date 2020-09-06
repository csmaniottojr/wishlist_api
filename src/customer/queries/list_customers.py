from sqlalchemy import select

from src.orm import customer as customer_table


def list_customers(sqla_session):
    customers = sqla_session.execute(select([customer_table])).fetchall()
    return [dict(customer) for customer in customers]
