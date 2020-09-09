from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.config import get_db_url

engine = create_engine(get_db_url(), echo=True)
session_factory = scoped_session(sessionmaker(bind=engine))
