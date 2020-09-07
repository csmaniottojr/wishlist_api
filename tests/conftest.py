import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from src.orm import metadata, start_mappers


@pytest.fixture
def sqla_memory_session():
    engine = create_engine('sqlite:///:memory:', echo=True)
    start_mappers()
    metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    clear_mappers()
