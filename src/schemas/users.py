from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    username: str = "noname"
    email: EmailStr


class UserCreate(UserBase):
    password: str | bytes


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
