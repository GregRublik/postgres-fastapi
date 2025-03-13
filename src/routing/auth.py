# from fastapi import APIRouter, Request
# from exeptions import (
#     TokenNoFoundException,
#     TokenExpiredException,
#     HTTPException,
#     UserAlreadyExistsException,
#     IncorrectEmailOrPasswordException,
#     PasswordMismatchException
# )
# from fastapi.responses import RedirectResponse
# from fastapi import APIRouter, Response
# from fastapi.requests import Request
# from app.users.auth import get_password_hash, authenticate_user, create_access_token
# from app.users.dao import UsersDAO
# from app.users.schemas import SUserRegister, SUserAuth
#
# auth = APIRouter(prefix='/auth', tags=['Auth'])
#
#
# @auth.post("/register/")
# async def register_user(user_data: SUserRegister) -> dict:
#     user = await UsersDAO.find_one_or_none(email=user_data.email)
#     if user:
#         raise UserAlreadyExistsException
#
#     if user_data.password != user_data.password_check:
#         raise PasswordMismatchException("Пароли не совпадают")
#     hashed_password = get_password_hash(user_data.password)
#     await UsersDAO.add(
#         name=user_data.name,
#         email=user_data.email,
#         hashed_password=hashed_password
#     )
#
#     return {'message': 'Вы успешно зарегистрированы!'}
#
#
# @auth.post("/login/")
# async def auth_user(response: Response, user_data: SUserAuth):
#     check = await authenticate_user(email=user_data.email, password=user_data.password)
#     if check is None:
#         raise IncorrectEmailOrPasswordException
#     access_token = create_access_token({"sub": str(check.id)})
#     response.set_cookie(key="users_access_token", value=access_token, httponly=True)
#     return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}
#
#
# @auth.post("/logout/")
# async def logout_user(response: Response):
#     response.delete_cookie(key="users_access_token")
#     return {'message': 'Пользователь успешно вышел из системы'}
#
#
# @auth.get("/")
# async def redirect_to_auth():
#     return RedirectResponse(url="/auth")
#
#
# @auth.exception_handler(TokenExpiredException)
# async def token_expired_exception_handler(request: Request, exc: HTTPException):
#     return RedirectResponse(url="/auth")
#
#
# @auth.exception_handler(TokenNoFoundException)
# async def token_no_found_exception_handler(request: Request, exc: HTTPException):
#     return RedirectResponse(url="/auth")
#
