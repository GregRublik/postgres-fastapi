from fastapi import APIRouter, Request, Depends, HTTPException, status, Cookie
from config import templates, settings, logger
from schemas.users import UserCreate, UserLogin
from fastapi.responses import RedirectResponse, Response

from typing import Annotated

from depends import users_service, get_jwt_service
from services.users import UserService
from services.jwt_services import JWTService, decode_jwt
from exeptions import (
    UserAlreadyExistsException,
    UserNoFoundException
)

auth = APIRouter()


async def get_current_user(
    access_token: str = Cookie(None, alias=settings.jwt.access_token_name),
    refresh_token: str = Cookie(None, alias=settings.jwt.refresh_token_name),
):
    try:
        access_token = await decode_jwt(token=access_token)
        refresh_token = await decode_jwt(token=refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error {e}")

    #  TODO Доработать проверку токенов (время истечение и прочее)


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
        jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
        response: Response
):
    try:
        db_user = await user_service.get_user_by_email(user)
    except UserNoFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User no found with this email"
        )
    if not await jwt_service.validate_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = await jwt_service.create_access_token(user)
    refresh_token = await jwt_service.create_refresh_token(user)
    response.set_cookie(settings.jwt.refresh_token_name, refresh_token)
    response.set_cookie(settings.jwt.access_token_name, access_token)
    return {'user': db_user}


@auth.post("/register")
async def register(
        user: UserCreate,
        user_service: Annotated[UserService, Depends(users_service)],
        jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
        response: Response
):
    hashed_password = await jwt_service.hash_password(user.password)
    user.password = hashed_password
    try:
        new_user = await user_service.add_user(user)
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists with this email'
        )
    access_token = await jwt_service.create_access_token(user)
    refresh_token = await jwt_service.create_refresh_token(user)
    response.set_cookie(
        key=settings.jwt.refresh_token_name,
        value=refresh_token
        )
    response.set_cookie(
        key=settings.jwt.access_token_name,
        value=access_token,
        # TODO Надо правильно настроить хранение токенов
        # httponly=True,  # Запрещает доступ к кукам через JavaScript (через document.cookie).
        # secure=settings.jwt.secure_cookies,  # Куки будут передаваться только по HTTPS соединению.
        # samesite=settings.jwt.same_site  # Контролирует отправку кук при межсайтовых запросах. (Strict|Lax|None)
    )

    return {'new_user': new_user}


@auth.get("/logout")
async def logout(response: Response):
    response.delete_cookie(settings.jwt.access_token_name)
    response.delete_cookie(settings.jwt.refresh_token_name)
    return {'status_code': 200}
