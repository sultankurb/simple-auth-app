from datetime import datetime, timedelta, timezone

import jwt

from src.settings import settings


async def encode_jwt(
    payload: dict,
    private_key: str =settings.auth.private_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_lifetime,
    expire_timedelta: timedelta | None = None
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm
    )
    return encoded


async def decode_jwt(
    token: str | bytes,
    algorithms: str = settings.auth.algorithm,
    public_key: str = settings.auth.public_key_path.read_text()
):
    return jwt.decode(jwt=token, key=public_key, algorithms=[algorithms])



async def create_jwt(
    token_type: str,
    token_type_field: str,
    token_data: dict,
    expire_minutes: int = settings.auth.access_token_lifetime,
    expire_timedelta: timedelta | None = None,
):
    jwt_payload = {token_type_field: token_type}
    jwt_payload.update(token_data)
    return await encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


async def create_access_token(user: dict):
    jwt_payload = {
        "sub": user["username"],
        "email": user["email"]
    }
    return await create_jwt(
        token_type="access",
        token_type_field="type",
        token_data=jwt_payload,
        expire_minutes=settings.auth.access_token_lifetime
    )


async def create_refresh_token(user: dict):
    jwt_payload = {
        "sub": user["email"]
    }
    return await create_jwt(
        token_type="refresh",
        token_type_field="type",
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth.refresh_token_lifetime),
    )
