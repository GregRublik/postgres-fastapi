
from typing import Union, Dict, Any
from repositories.repository import AbstractRepository, RabbitMQRepository
from schemas.users import UserCreate, UserLogin, User
from exeptions import (
    UserAlreadyExistsException,
    ModelAlreadyExistsException,
    ModelNoFoundException,
    UserNoFoundException
)


class BrokerService:

    def __init__(self, repository: Union[AbstractRepository, RabbitMQRepository]):
        self.repository = repository

    # todo надо сделать чтобы возвращал результат по идее
    async def add_message(self, queue_name: str, message: Dict[str, Any], **kwargs):

        try:
            await self.repository.add_one(queue_name, message, **kwargs)
        except Exception:  # todo в случае если произошла ошибка добавления сообщения надо что-то делать
            print("exception")

    # todo естественно надо доработать функции поиска и получения сообщений

    # async def get_user_by_email(self, user: UserLogin) -> User:
    #     user_dict = user.model_dump()
    #
    #     try:
    #         found_user = await self.repository.find_one_by_email(self.session, user_dict)
    #         return found_user
    #     except ModelNoFoundException:
    #         raise UserNoFoundException
    #
    # async def get_message(self, user: User) -> User:
    #     user_dict = user.model_dump()
    #
    #     try:
    #         found_user = await self.repository.find_one(self.session, user_dict)
    #         return found_user
    #     except ModelNoFoundException:
    #         raise UserNoFoundException
