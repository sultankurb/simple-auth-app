from fastapi import APIRouter

from src.routers.admin.router import admin
from src.routers.users.router import users
from src.settings import settings

api_routers = APIRouter(
    prefix=settings.api_prefix
)
api_routers.include_router(router=users)
api_routers.include_router(router=admin)
