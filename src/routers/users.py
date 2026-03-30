from fastapi import APIRouter

from src.db.models.users import fastapi_users
from src.schemas.users import UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["users"],
)
