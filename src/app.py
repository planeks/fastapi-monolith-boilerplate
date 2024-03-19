import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.settings import settings
from src.routers import api_router

app = FastAPI()

app.include_router(api_router, prefix=settings.api_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main() -> None:
    """Runs the FastAPI application."""
    uvicorn.run(
        app="src.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload
    )


if __name__ == "__main__":
    main()
