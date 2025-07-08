from typing import Annotated

from config import engine
from fastapi import Depends
from sqlmodel import Session, SQLModel


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
