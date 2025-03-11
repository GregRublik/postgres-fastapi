from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query

from depends import messages_service
from schemas.messages import MessageCreate, MessageResponse
from services.messages import MessageService

messages = APIRouter(prefix="/messages", tags=["messages"])


@messages.post("/add")
async def add_one(
        message: MessageCreate,
        message_service: Annotated[MessageService, Depends(messages_service)]
):
   message_id = await message_service.add_message(message)
   return {"message_id": message_id}


@messages.get("/history/{chat_id}", response_model=List[MessageResponse])
def get_chat_history(
    chat_id: int,
    limit: Optional[int] = Query(10, ge=1, description="Количество сообщений на странице"),
    offset: Optional[int] = Query(0, ge=0, description="Смещение для пагинации"),
    db: Session = Depends(get_db)
):
    # Проверяем, существует ли чат с указанным ID
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    # Получаем сообщения для указанного чата с пагинацией и сортировкой
    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(asc(Message.timestamp))  # Сортировка по времени отправки (по возрастанию)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return messages

# @main.post("/get_all")
# async def get_all(main: MainSchema, main_service: Annotated[MainService, Depends(main_service)]) -> MainSchema:
#    book = book_service.create_book()
#    return book
