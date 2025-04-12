from pathlib import Path

from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    DB_URL: str = None
    ADMIN_PASSWORD: str = None
    ADMIN_EMAIL: EmailStr = None
    auth: JWTModel = JWTModel()


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
