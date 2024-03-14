from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.ext.declarative import declarative_base
from src.settings import settings

SQLALCHEMY_DB_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@"
    f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)
async_session_maker = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Returns async db session

    Yields:
        Iterator[AsyncGenerator[AsyncSession, None]]: Async db session
    """
    async with async_session_maker() as session:
        yield session
