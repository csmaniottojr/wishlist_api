from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from src.customer.domain import entities

metadata = MetaData()

customer = Table(
    'customer',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100)),
    Column('email', String(100)),
)

wished_product = Table(
    'wished_product',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', Integer, ForeignKey('customer.id')),
    Column('product_id', String(36)),
)


def start_mappers():
    mapper(
        entities.Customer,
        customer,
        properties={
            'wishlist': relationship(
                entities.WishedProduct, cascade='all, delete', collection_class=set
            )
        },
    )

    mapper(entities.WishedProduct, wished_product)
