from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str = "noname"
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
