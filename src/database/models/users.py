from enum import Enum
from typing import List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr


class RoleEnum(Enum):
    admin = "admin"
    user = "user"
    staff = "staff"


class UsersBaseModel(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    links: Optional[List[str]] = None
    is_banned: bool = False
    role: RoleEnum = RoleEnum.user



class UsersCreate(UsersBaseModel):
    password: str



class UsersRead(UsersBaseModel):
    _id: Optional[PydanticObjectId] = None
    media_url: Optional[List[str]] = None

    class Config:
        from_attributes = True


class UsersUpdate(UsersBaseModel):
    pass


class UpdatePassword(BaseModel):
    old_password: Optional[str] = None
    new_password: Optional[str] = None
    confirm_password: Optional[str] = None



class UsersODM(UsersCreate, Document):
    media_url: Optional[List[str]] = None

    class Setting:
        name = "users"


class TokenData(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
