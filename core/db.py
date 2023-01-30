from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from functools import lru_cache
from typing import Generator
from config import Settings
import os
from alembic import command
from alembic.config import Config
from sqlalchemy_utils import create_database, database_exists


testing = os.environ.get("TESTING")
if testing:
    # для локального использования
    #SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:space@localhost/restoran_pytest"
    # для docker  с приложением
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:space@restoran_db/restoran_pytest"
    # для docker с тестами
    #SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:space@restoran_pytest/restoran_pytest"

else:

    # для docker compose
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:space@restoran_db/restoran_m"
    # для localhost
    #SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:space@localhost/restoran_m"
    # для тестов в docker
    #SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:space@restoran_pytest/restoran_m"

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)
    # engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
# SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()


@lru_cache
def create_session() -> scoped_session:
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine),
    )
    return session


def get_db() -> Generator[scoped_session, None, None]:
    session = create_session()
    try:
        yield session
    finally:
        session.remove()


"""
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:space@localhost/restoran_m"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
