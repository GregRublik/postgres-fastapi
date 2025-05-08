from fastapi import Cookie, APIRouter, Request, WebSocket, Depends, status, HTTPException
from depends import get_broker_service
from typing import Dict, Annotated
from config import templates
from schemas.messages import ReadMessage, CreateMessage
from services.broker import BrokerService
from exceptions import QueueEmptyException, MessageConsumeException

main = APIRouter(tags=["main"])

active_connections: Dict[int, WebSocket] = {}


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


@main.post("/create_rabbit_message/")
async def create_rabbit_message(
    broker_service: Annotated[BrokerService, Depends(get_broker_service)],
    message: CreateMessage
):
    return await broker_service.publish_message(message.queue_name, message.message)


@main.post("/read_rabbit_message")
async def read_rabbit_message(
    broker_service: Annotated[BrokerService, Depends(get_broker_service)],
    message: ReadMessage
):
    try:
        return await broker_service.get_single_message(message)
    except QueueEmptyException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "error": "Message no found with this name"}
        )
    except MessageConsumeException:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail={"success": False, "error": "Ошибка при поиске сообщения"}
        )
