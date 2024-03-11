import uvicorn
from fastapi import FastAPI

from settings import settings
from src.db.config import create_db_and_tables
from src.schemas.users import UserRead, UserUpdate, UserCreate
from src.db.models.users import auth_backend, current_active_user, fastapi_users

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


def main() -> None:
    uvicorn.run(
        app="src.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload
    )


if __name__ == "__main__":
    main()
