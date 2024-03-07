from uuid import UUID as UUID_T
from sqlalchemy import (
    Boolean,
    Column,
    String,
    UUID,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.config import Base


class User(Base):
    
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    

async def get_user(db: AsyncSession, user_id: UUID_T) -> User:
    return await db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: AsyncSession, email: str) -> User:
    return db.query(User).filter(User.email == email).first()
