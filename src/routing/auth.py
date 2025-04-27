from fastapi import APIRouter, Request, Depends, HTTPException, status, Cookie
from config import templates, settings
from schemas.users import UserCreate, UserLogin, User
from fastapi.responses import Response

from typing import Annotated

from depends import get_user_service, get_jwt_service
from services.users import UserService
from services.jwt_services import JWTService, decode_jwt
from jwt.exceptions import ExpiredSignatureError
from exeptions import (
    UserAlreadyExistsException,
    UserNoFoundException
)


auth = APIRouter(tags=["auth"])


async def get_current_user(
    response: Response,
    user_service: Annotated[UserService, Depends(get_user_service)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
    access_token: str = Cookie(None, alias=settings.jwt.access_token_name),
    refresh_token: str = Cookie(None, alias=settings.jwt.refresh_token_name),
):
    if not access_token or not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "error": "tokens is not exist"}
        )
    # todo надо продумать получше логику проверки пользователя и токенов.
    try:
        await decode_jwt(token=access_token)
    except ExpiredSignatureError:
        try:
            decoded_refresh_token = await decode_jwt(token=refresh_token)

            db_user = await user_service.get_user(User(id=decoded_refresh_token.get("sub"), **decoded_refresh_token))
            response.set_cookie(
                key=settings.jwt.access_token_name,
                value=await jwt_service.create_access_token(db_user),
            )
            response.set_cookie(
                key=settings.jwt.refresh_token_name,
                value=await jwt_service.create_refresh_token(db_user),
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"success": False, "error": "Session expired. Re-login required"}
            )


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
        user_service: Annotated[UserService, Depends(get_user_service)],
        jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
        response: Response
):
    try:
        db_user = await user_service.get_user_by_email(user)
    except UserNoFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            # success=False,
            detail={"success": False, "error": "User no found with this email"}
        )
    if not await jwt_service.validate_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"success": False, "error": "Invalid credentials"}
        )
    response.set_cookie(settings.jwt.refresh_token_name, await jwt_service.create_refresh_token(db_user))
    response.set_cookie(settings.jwt.access_token_name, await jwt_service.create_access_token(db_user))
    del db_user.password
    return {"detail": {"success": True, 'user': db_user}}


@auth.post("/register")
async def register(
        user: UserCreate,
        user_service: Annotated[UserService, Depends(get_user_service)],
        jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
        response: Response
):
    user.password = await jwt_service.hash_password(user.password)
    try:
        new_user = await user_service.add_user(user)
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"success": False, "error": "User already exists with this email"}
        )
    response.set_cookie(
        key=settings.jwt.refresh_token_name,
        value=await jwt_service.create_refresh_token(new_user)
        )
    response.set_cookie(
        key=settings.jwt.access_token_name,
        value=await jwt_service.create_access_token(new_user),
        # TODO Надо правильно настроить хранение токенов
        # httponly=True,  # Запрещает доступ к кукам через JavaScript (через document.cookie).
        # secure=settings.jwt.secure_cookies,  # Куки будут передаваться только по HTTPS соединению.
        # samesite=settings.jwt.same_site  # Контролирует отправку кук при "меж сайтовых" запросах. (Strict|Lax|None)
    )
    del new_user.password
    return {"detail": {"success": True, 'new_user': new_user}}


@auth.get("/logout")
async def logout(response: Response):
    response.delete_cookie(settings.jwt.access_token_name)
    response.delete_cookie(settings.jwt.refresh_token_name)
    return {"detail": {"success": True, "message": "Logged out successfully"}}
