from repositories.repository import AbstractRepository
from schemas.chats import ChatCreate, Chat


class ChatService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add_chat(self, chat: ChatCreate):
        chat_dict = chat.model_dump()
        chat_id = await self.repository.add_one(chat_dict)
        return chat_id

    async def find_all(self, chat: Chat):
        result = self.repository.find_all()
        return result
