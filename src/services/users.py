from repositories.repository import AbstractRepository
from schemas.users import UserCreate, User


class UserService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add_user(self, user: UserCreate):
        user_dict = user.model_dump()
        user_id = await self.repository.add_one(user_dict)
        return user_id

    # async def find_all(self, user: User):
    #     result = self.repository.find_all()
    #     return result
