from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from models.user import UserModel
from settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):  # noqa: B008
    yield SQLModelUserDatabaseAsync(session, UserModel)
