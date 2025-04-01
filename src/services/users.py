from repositories.repository import AbstractRepository, UserRepository
from schemas.users import UserCreate, UserLogin
from config import settings
from exeptions import UserAlreadyExistsException, ModelAlreadyExistsException


class UserService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add_user(self, user: UserCreate):
        user_dict = user.model_dump()

        try:
            new_user = await self.repository.add_one(user_dict)
            return new_user
        except ModelAlreadyExistsException:
            raise UserAlreadyExistsException

    async def get_user_by_email(self, user: UserLogin):
        user_dict = user.model_dump()

        try:
            user = await self.repository.find_one({"email": user.email})
            return user
        except ModelAlreadyExistsException:  # нужно заменить на ошибку "пользователь не найден"
            raise UserAlreadyExistsException  # нужно вызывать другую ошибку


