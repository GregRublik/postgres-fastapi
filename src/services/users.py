from repositories.repository import AbstractRepository, UserRepository
from schemas.users import UserCreate, UserLogin
from config import settings


class UserService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add_user(self, user: UserCreate):
        user_dict = user.model_dump()
        user_id = await self.repository.add_one(user_dict)
        return user_id

    # async def create_token(self, user: UserLogin):
    #     user_dict = user.model_dump()
    #     print(user_dict)
    #     return '1234'
    #     # user_id = await self.repository.find_one(user_dict)
    #     # token = await settings.security.create_access_token(uid=user_dict['name'])
    #     # return token
