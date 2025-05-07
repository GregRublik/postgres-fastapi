from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union
from repositories.repository import AbstractRepository, UserRepository
from schemas.users import UserCreate, UserLogin, User
from exceptions import (
    UserAlreadyExistsException,
    ModelAlreadyExistsException,
    ModelNoFoundException,
    UserNoFoundException
)


class UserService:

    def __init__(self, repository: Union[AbstractRepository, UserRepository], session: AsyncSession):
        self.repository = repository
        self.session = session

    async def add_user(self, user: UserCreate) -> User:
        user_dict = user.model_dump()

        try:
            new_user = await self.repository.add_one(self.session, user_dict)
            return new_user
        except ModelAlreadyExistsException:
            raise UserAlreadyExistsException

    async def get_user_by_email(self, user: UserLogin) -> User:
        user_dict = user.model_dump()

        try:
            found_user = await self.repository.find_one_by_email(self.session, user_dict)
            return found_user
        except ModelNoFoundException:
            raise UserNoFoundException

    async def get_user(self, user: User) -> User:
        user_dict = user.model_dump()

        try:
            found_user = await self.repository.find_one(self.session, user_dict)
            return found_user
        except ModelNoFoundException:
            raise UserNoFoundException
