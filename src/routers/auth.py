from fastapi import APIRouter
from src.schemas.users import UserRead, UserCreate
from src.db.models.users import auth_backend, fastapi_users

router = APIRouter()

router.include_router(
    router=fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"]
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
