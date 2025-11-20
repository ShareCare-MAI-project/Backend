from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import DATABASE_URL

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    future=True,
    pool_pre_ping=True,
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base for models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency для получения сессии БД.
    
    Используется в FastAPI для автоматического внедрения сессии в маршруты.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def default_async_db_request(query):
    """
    Выполнить асинхронный запрос к БД.
    
    Args:
        query: SQLAlchemy query объект
    
    Returns:
        Результат запроса
    """
    async with async_session() as session:
        result = await session.execute(query)
        return result.scalars().all()


async def init_db():
    """Инициализировать БД (создать все таблицы)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Закрыть соединение с БД"""
    await engine.dispose()