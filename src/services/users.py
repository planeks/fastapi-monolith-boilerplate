import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID as UUID_T

from src.db.models.users import User
from src.services.utils import get_hashed_password


async def get_user(db: AsyncSession, user_id: UUID_T) -> User:
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def create_db_user(db: AsyncSession, email: str, password: str) -> User:
    existing_user = await get_user_by_email(db, email)
    if not existing_user:
        new_user = User(id=uuid.uuid4(), email=email, hashed_password=get_hashed_password(password), is_active=True)
        db.add(new_user)
        await db.commit()
        return new_user
