from fastapi import APIRouter, Request, Depends
from authx import AuthX, AuthXConfig
from config import templates
from schemas.users import UserCreate
from fastapi.responses import RedirectResponse

from typing import Annotated

from depends import users_service
from services.users import UserService

auth = APIRouter()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


@auth.get("/login")
async def login(
        request: Request
):
    return templates.TemplateResponse(
        request,
        name="auth.html",
        context={}
    )


@auth.get("/register")
async def register(
        user: UserCreate,
        user_service: Annotated[UserService, Depends(users_service)]
):
    await user_service.add_user(user)
    return RedirectResponse("/")

