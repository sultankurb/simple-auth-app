from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env"
    )
    DB_URL: str = None
    ADMIN_PASSWORD: str = None
    ADMIN_EMAIL: EmailStr = None


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
