# from typing import Annotated, List, Optional
#
# from fastapi import APIRouter, Depends, Query, Request
# from config import settings
# from depends import messages_service
# from schemas.messages import MessageCreate, Message, MessageHistory
# from services.messages import MessageService
#
# messages = APIRouter(prefix="/messages", tags=["messages"])
#
#
# @messages.post("/add")
# async def add_one(
#         message: MessageCreate,
#         message_service: Annotated[MessageService, Depends(messages_service)]
# ):
#     message_id = await message_service.add_message(message)
#     return {"message_id": message_id}
#
#
# @messages.get("/history/{chat_id}", response_model=List[Message])
# async def get_chat_history(
#         chat: MessageHistory,
#         message_service: Annotated[MessageService, Depends(messages_service)],
# ):
#     history = await message_service.find_history(chat)
#     return {"history": history}
#
#
# # Получение сообщений между двумя пользователями
# @messages.get(
#     "/{user_id}",
#     response_model=List[Message],
#     dependencies=[Depends(settings.security.access_token_required)],
#
# )
# async def get_messages(
#         user_id: int,
#         message_service: Annotated[MessageService, Depends(messages_service)],
#         request: Request
# ):
#     settings.security.get_dependency(request)
#     # Возвращаем список сообщений между текущим пользователем и другим пользователем
#     return await message_service.find_history(user_id_1=user_id, user_id_2=message_service.id) or []
