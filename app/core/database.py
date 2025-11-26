from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_DB


class Base(DeclarativeBase):
    pass


# host всегда 'postgres' потому что сервер и БД в одном контейнере
SYNC_POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:{POSTGRES_PORT}/{POSTGRES_DB}"
ASYNC_POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:{POSTGRES_PORT}/{POSTGRES_DB}"

async_engine = create_async_engine(ASYNC_POSTGRES_URL, echo=True)
sync_engine = create_engine(SYNC_POSTGRES_URL, echo=True)


def create_db_and_tables() -> None:
    Base.metadata.create_all(sync_engine)


def setup_db() -> None:
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)
    create_db_and_tables()


async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            # откатываем все изменения при ошибке
            await session.rollback()
            raise
        finally:
            await session.close()
