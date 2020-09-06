from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper

from src.customer.domain import entities

metadata = MetaData()

customer = Table(
    'customer',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('email', String(100)),
)

mapper(entities.Customer, customer)
