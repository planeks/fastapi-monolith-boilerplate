from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

SQLALCHEMY_DB_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)
async_session_maker = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    """Returns async db session

    Yields:
        Iterator[AsyncGenerator[AsyncSession, None]]: Async db session
    """
    async with async_session_maker() as session:
        yield session
