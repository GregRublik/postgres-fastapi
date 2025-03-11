from repositories.repository import AbstractRepository
from schemas.messages import MessageCreate, Message


class MessageService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add_message(self, message: MessageCreate):
        message_dict = message.model_dump()
        message_id = await self.repository.add_one(message_dict)
        return message_id

    async def find_all(self, message: Message):
        result = self.repository.find_all()
        return result
