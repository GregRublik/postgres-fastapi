from fastapi import Cookie, APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from typing import Dict, Annotated
from auth import get_current_user
from config import settings, templates
import asyncio

main = APIRouter(tags=["main"])

active_connections: Dict[int, WebSocket] = {}


# @main.get("/", dependencies=[Depends(settings.security.access_token_required)])
@main.get("/")
async def index(
        request: Request,
        cookie: Annotated[str | None, Cookie()] = None
):
    print(cookie)
    return templates.TemplateResponse(request, "chat.html", context={
        'user': {'id': '1'},
        'users_all': [{'id': '2', 'name': 'zalupa'}]
    })


# # WebSocket эндпоинт для соединений
# @main.websocket("/ws/{user_id}", dependencies=[Depends(settings.security.access_token_required)])
# async def websocket_endpoint(websocket: WebSocket, user_id: int):
#     # Принимаем WebSocket-соединение
#     await websocket.accept()
#     # Сохраняем активное соединение для пользователя
#     active_connections[user_id] = websocket
#     try:
#         while True:
#             # Просто поддерживаем соединение активным (1 секунда паузы)
#             await asyncio.sleep(1)
#     except WebSocketDisconnect:
#         # Удаляем пользователя из активных соединений при отключении
#         active_connections.pop(user_id, None)
