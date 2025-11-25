from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy_utils import database_exists, create_database

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


AsyncSession = async_sessionmaker(async_engine, expire_on_commit=False)


def get_db():
    db = Session(sync_engine)
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    async with AsyncSession() as session:
        yield session


async def default_async_db_request(request):
    """
    Функция-обёртка для дефолтных запросов в БД (rollback при ошибке и commit если всё ок)
    
    Пример:
        await default_async_db_request(user.create_user)
    
    ВАЖНО: Прокидывает ошибку наверх если что-то пошло не так
    """
    async with AsyncSession() as session:
        try:
            result = request(session)
            # если результат асинхронный — ждём его
            if hasattr(result, '__await__'):
                result = await result
            # коммитим если всё ок
            await session.commit()
            return result
        except Exception as e:
            # откатываем все изменения при ошибке
            await session.rollback()
            raise


def sync_db_request(request_func, *args, **kwargs):
    """
    Простой синхронный запрос к БД (для случаев если нужен sync, а не async)
    
    Пример:
        result = sync_db_request(create_user, user_data)
    """
    db = Session(sync_engine)
    try:
        result = request_func(db, *args, **kwargs)
        db.commit()
        return result
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()