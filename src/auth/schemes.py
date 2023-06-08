import uuid
from typing import Optional
from fastapi_users.authentication.transport.bearer import BearerResponse
from fastapi import UploadFile
from fastapi_users import schemas
from pydantic import BaseModel
from sqlalchemy_file import FileField
from sqlalchemy_file.validators import ContentTypeValidator


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: int
    username: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False






