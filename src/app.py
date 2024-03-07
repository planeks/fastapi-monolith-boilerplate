import uvicorn
from fastapi import FastAPI

from settings import settings


app = FastAPI()


def main() -> None:
    uvicorn.run(
        app="src.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_reload
    )
    

if __name__ == "__main__":
    main()
