from typing import Annotated

from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database.models.users import PasswordUpdate, RoleEnum, UsersODM
from src.services.auth.jwt_service import (
    create_access_token,
    create_refresh_token,
    decode_jwt,
)

from .crud import UsersRepository
from .hash_password import check_password, hash_password

repository = UsersRepository()

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login/"
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)]
):
    payload = await decode_jwt(token=token)
    username: str = payload.get("sub")
    user = await repository.get_one(filters={"username": username})
    return user


async def get_active_current_user(
    user: Annotated[
        UsersODM, 
        Depends(get_current_user)
    ]
):
    if user.is_banned is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You have been banned"
        )
    return user


async def get_admin_users(
    user: Annotated[
        UsersODM,
        Depends(get_active_current_user)
    ]
):
    if user.role is not RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user


async def sign_in(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends()
):
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="invalid username or password"
    )
    check = await repository.get_one(filters={"username": form.username})
    if check is None:
        raise exception
    if not check_password(
        passowrd=form.password, 
        hashed_password=check.password
    ):
            raise exception
    access_token = await create_access_token(
        user={
            "username": check.username,
            "email": check.email,
        }    
    )
    refresh_token = await create_refresh_token(
        user={
            "username": check.username,
            "email": check.email,
        }
    )
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True
    )
    response.set_cookie(
        key="refresh_token", 
        value=f"Bearer {refresh_token}", 
        httponly=True
    )
    return [access_token, refresh_token]


async def sign_out(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")



async def register_user(user: UsersODM):
    check = await repository.get_one(
        filters={"username": user.username, "email": user.email}
    )
    if check is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username or email is already used try another"
        )
    user.password = hash_password(password=user.password)
    result = await repository.add_one(data=user)
    return result



async def update_password(
    schema: PasswordUpdate,
    user: Annotated[UsersODM, Depends(get_active_current_user)]
):
    if not check_password(
        passowrd=schema.old_password,
        hashed_password=user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorect password"
        )
    if schema.new_password != schema.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirn password not same"
        )
    data: dict = schema.model_dump()
    new_hashed_password = hash_password(password=data.get("new_password"))
    result = await repository.update_one(
        filters={"username": user.username},
        data={"password": new_hashed_password}
    )
    if result is True:
        return {"Message": "Password was updated"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Something went wrog, try again later"
    )
