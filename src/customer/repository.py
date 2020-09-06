from sqlalchemy import exists
from sqlalchemy.orm import Session

from src.customer.domain.entities import Customer


class SQLACustomerRepository:
    def __init__(self, sqla_session: Session):
        self.sqla_session = sqla_session

    def get_by_id(self, customer_id):
        return (
            self.sqla_session.query(Customer)
            .filter(Customer.id == customer_id)
            .one_or_none()
        )

    def get_by_email(self, email):
        return (
            self.sqla_session.query(Customer)
            .filter(Customer.email == email)
            .one_or_none()
        )

    def has_customer_with_email(self, email):
        stmt = exists().where(Customer.email == email)
        return self.sqla_session.query(stmt).scalar()

    def save(self, customer):
        self.sqla_session.add(customer)
        self.sqla_session.commit()

    def delete(self, customer):
        self.sqla_session.delete(customer)
        self.sqla_session.commit()
