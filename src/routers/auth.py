from fastapi import APIRouter

from src.db.models.users import auth_backend, fastapi_users
from src.schemas.users import UserCreate, UserRead

router = APIRouter()

router.include_router(
    router=fastapi_users.get_auth_router(auth_backend), prefix="/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["auth"],
)
