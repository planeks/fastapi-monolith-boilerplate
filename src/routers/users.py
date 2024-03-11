from fastapi import APIRouter

from src.schemas.users import UserRead, UserUpdate
from src.db.models.users import fastapi_users

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["users"],
)
