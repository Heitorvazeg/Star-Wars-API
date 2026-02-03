from fastapi import FastAPI

from app.router import router as api_router
from core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Star Wars API",
        version="1.0.0",
        debug=settings.DEBUG,
    )

    app.include_router(api_router)

    return app
