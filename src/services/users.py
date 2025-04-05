from repositories.repository import AbstractRepository
from schemas.users import UserCreate, UserLogin, User
from exeptions import (
    UserAlreadyExistsException,
    ModelAlreadyExistsException,
    ModelNoFoundException,
    UserNoFoundException
)
from config import logger


class UserService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add_user(self, user: UserCreate) -> User:
        user_dict = user.model_dump()

        try:
            new_user = await self.repository.add_one(user_dict)
            logger.info(new_user)
            return new_user
        except ModelAlreadyExistsException:
            raise UserAlreadyExistsException

    async def get_user_by_email(self, user: UserLogin):

        user_dict = user.model_dump()
        try:
            found_user = await self.repository.find_one(user_dict)
            return found_user
        except ModelNoFoundException:
            raise UserNoFoundException

