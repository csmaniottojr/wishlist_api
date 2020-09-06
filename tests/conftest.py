import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.orm import metadata


@pytest.fixture
def sqla_memory_session():
    engine = create_engine('sqlite:///:memory:', echo=True)
    metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    return session_factory()
