from fastapi import APIRouter, Request, Depends, HTTPException, status
from config import templates, settings
from schemas.users import UserCreate, UserLogin
from fastapi.responses import RedirectResponse, Response

from typing import Annotated

from depends import users_service
from services.users import UserService
from exeptions import UserAlreadyExistsException

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
    return {}


@auth.post("/register")
async def register(
        user: UserCreate,
        user_service: Annotated[UserService, Depends(users_service)],
        response: Response
):
    print(user.model_dump())
    try:
        new_user = await user_service.add_user(user)
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists with this email'
        )
    refresh_token = "refresh_token1234"
    access_token = "access_token1234"
    response.set_cookie(settings.jwt.refresh_token_name, refresh_token)
    response.set_cookie(settings.jwt.access_token_name, access_token)

    return {'new_user': new_user}
