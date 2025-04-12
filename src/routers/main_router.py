from fastapi import APIRouter

from src.settings import settings

api_routers = APIRouter(
    prefix=settings.api_prefix
)
