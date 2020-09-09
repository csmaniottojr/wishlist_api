import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from src.orm import metadata, start_mappers
from tests.functional_tests.auth import api as auth_api


@pytest.fixture
def sqla_memory_session():
    engine = create_engine('sqlite:///:memory:', echo=True)
    start_mappers()
    metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    clear_mappers()


@pytest.fixture(scope='session')
def access_token():
    email = 'functionaltests@test.com'
    password = 'password'

    auth_api.signup(email, password)
    response = auth_api.login(email, password)
    return response.json()['token']
