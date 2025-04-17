from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from src.database.models.users import (
    PasswordUpdate,
    TokenData,
    UsersODM,
    UsersRead,
)
from src.services.auth.auth_logic import (
    get_active_current_user,
    register_user,
    sign_in,
    sign_out,
    update_password,
)

users = APIRouter(
    prefix='/users',
    tags=['user'],
)


@users.post(path="/login/", response_model=TokenData)
async def sign_in_user(
    response: Response,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    result = await sign_in(response=response, form=form)
    return TokenData(access_token=result[0], refresh_token=result[1])


@users.post(
    path="/register/new/user/",
    status_code=status.HTTP_201_CREATED,
    response_model=UsersRead
)
async def register_new_user(schema: UsersODM):
    result = await register_user(user=schema)
    return result


@users.get(path="/get/current/user/", response_model=UsersRead)
async def get_current_user(
    user: Annotated[
        UsersODM,
        Depends(get_active_current_user)
    ]
):
    return user


@users.post(path="/sign/out/")
async def sign_out_one_user(
    response: Response,
    user: Annotated[
        UsersODM,
        Depends(get_active_current_user)
        ]
    ):
    await sign_out(response=response)
    username = user.username
    return {"Message": f"Good bye {username}"}


@users.post(path="/upload/media/")
async def upload_media():
    #TODO
    pass


@users.put(path="/update/password/")
async def update_mine_password(
    schema: PasswordUpdate,
    user: Annotated[
        UsersODM, Depends(get_active_current_user)
    ]
):
    result = await update_password(schema=schema, user=user)
    return result
