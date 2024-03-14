import uvicorn
from fastapi import FastAPI

from src.settings import settings
from src.routers import api_router

app = FastAPI()

app.include_router(api_router, prefix=settings.api_prefix)

def main() -> None:
    uvicorn.run(
        app="src.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload
    )


if __name__ == "__main__":
    main()
