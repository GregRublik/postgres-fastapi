from typing import Annotated

from fastapi import APIRouter, Depends

from depends import users_service
from schemas.users import UserCreate
from services.users import UserService

users = APIRouter(prefix="/users", tags=["users"])


@users.post("/add")
async def add_one(
        user: UserCreate,
        user_service: Annotated[UserService, Depends(users_service)]
):
    user_id = await user_service.add_user(user)
    return {"user_id": user_id}


# @main.post("/get_all")
# async def get_all(main: MainSchema, main_service: Annotated[MainService, Depends(main_service)]) -> MainSchema:
#    book = book_service.create_book()
#    return book
