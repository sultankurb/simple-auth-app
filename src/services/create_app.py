from fastapi import FastAPI

from src.services.middleware import register_middleware
from src.settings import lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title='This service for manage users',
        version="0.1",
    )
    register_middleware(app)

    return app
