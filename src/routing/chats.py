from typing import Annotated

from fastapi import APIRouter, Depends

from depends import chats_service
from schemas.chats import ChatCreate
from services.chats import ChatService

chats = APIRouter(prefix="/chats", tags=["chats"])


@chats.post("/add")
async def add_one(
        chat: ChatCreate,
        chat_service: Annotated[ChatService, Depends(chats_service)]
):
    chat_id = await chat_service.add_chat(chat)
    return {"chat_id": chat_id}

# @main.post("/get_all")
# async def get_all(main: MainSchema, main_service: Annotated[MainService, Depends(main_service)]) -> MainSchema:
#    book = book_service.create_book()
#    return book
