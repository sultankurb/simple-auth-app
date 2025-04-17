from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Optional

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.database.models.users import UsersODM

BASE_DIR = Path(__file__).parent.parent


class JWTModel(BaseModel):
    public_key_path: Path = BASE_DIR / "certificates" / "public-key.pem"
    private_key_path: Path = BASE_DIR / "certificates" / "private-key.pem"
    access_token_lifetime: int = 15
    refresh_token_lifetime: int = 30
    algorithm: str = "RS256"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env"
    )
    api_prefix: str = "/api/v1"
    DB_URL: Optional[str] = None
    ADMIN_PASSWORD: Optional[str] = None
    ADMIN_EMAIL: Optional[EmailStr] = None
    auth: JWTModel = JWTModel()

    async def init_database(self):
        clent = AsyncIOMotorClient(self.DB_URL)
        await init_beanie(
            database=clent["auth-app"],
            document_models=[UsersODM]
        )


def get_settings() -> Settings:
    return Settings()


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await settings.init_database()
    yield
