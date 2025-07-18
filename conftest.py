import os

import pytest
from sqlalchemy import create_engine
from sqlmodel import Session

import settings  # noqa
from alembic import command
from alembic.config import Config

# Use SYNC SQLite driver for Alembic and testing
TEST_DATABASE_URL = "sqlite:///./test_database.db"


@pytest.fixture(scope="session")
def engine():
    os.environ["TEST_DATABASE_URL"] = TEST_DATABASE_URL
    engine = create_engine(TEST_DATABASE_URL, echo=False)

    # Run migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield engine


@pytest.fixture(scope="function")
def session(engine):
    connection = engine.connect()
    trans = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    trans.rollback()
    connection.close()
