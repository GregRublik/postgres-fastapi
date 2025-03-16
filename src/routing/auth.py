from fastapi import APIRouter, Request, Depends
from config import templates, settings
from schemas.users import UserCreate, UserLogin
from fastapi.responses import RedirectResponse, Response

from typing import Annotated

from depends import users_service
from services.users import UserService

auth = APIRouter()


@auth.get("/auth")
async def authorization(
        request: Request
):
    return templates.TemplateResponse(
        request,
        name="auth.html",
        context={}
    )


@auth.post("/login")
async def login(
        user: UserLogin,
        user_service: Annotated[UserService, Depends(users_service)],
        response: Response
):
    print(user.model_dump())
    # token = await user_service.create_token(user)
    token = "token1234"
    response.set_cookie(settings.security.config.JWT_ACCESS_COOKIE_NAME, token)
    return RedirectResponse("/")


@auth.post("/register")
async def register(
        user: UserCreate,
        user_service: Annotated[UserService, Depends(users_service)]
):
    print(user.model_dump())
    await user_service.add_user(user)
    return RedirectResponse("/auth")
