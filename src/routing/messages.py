from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query

from depends import messages_service
from schemas.messages import MessageCreate, Message, MessageHistory
from services.messages import MessageService

messages = APIRouter(prefix="/messages", tags=["messages"])


@messages.post("/add")
async def add_one(
        message: MessageCreate,
        message_service: Annotated[MessageService, Depends(messages_service)]
):
    message_id = await message_service.add_message(message)
    return {"message_id": message_id}


@messages.get("/history/{chat_id}", response_model=List[Message])
async def get_chat_history(
        chat: MessageHistory,
        message_service: Annotated[MessageService, Depends(messages_service)],
):
    history = await message_service.find_history(chat)
    return {"history": history}
    # # Проверяем, существует ли чат с указанным ID
    # chat = db.query(Chat).filter(Chat.id == chat_id).first()
    # if not chat:
    #     raise HTTPException(status_code=404, detail="Чат не найден")
    #
    # # Получаем сообщения для указанного чата с пагинацией и сортировкой
    # messages = (
    #     db.query(Message)
    #     .filter(Message.chat_id == chat_id)
    #     .order_by(asc(Message.timestamp))  # Сортировка по времени отправки (по возрастанию)
    #     .offset(offset)
    #     .limit(limit)
    #     .all()
    # )
    #
    # return messages

# @main.post("/get_all")
# async def get_all(main: MainSchema, main_service: Annotated[MainService, Depends(main_service)]) -> MainSchema:
#    book = book_service.create_book()
#    return book
