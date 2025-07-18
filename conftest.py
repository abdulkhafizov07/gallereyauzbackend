import os

import pytest
from sqlalchemy import create_engine
from sqlmodel import Session

from alembic import command
from alembic.config import Config

TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///test_db.sqlite3")


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL, echo=False)

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
