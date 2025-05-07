from fastapi import Cookie, APIRouter, Request, WebSocket, Depends, status, HTTPException
from depends import get_broker_service
from typing import Dict, Annotated
from config import templates
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
):
    new_message = await broker_service.publish_message("first_message", {"detail": 1, "comment": "good"})
    return new_message

@main.get("/reed_rabbit_message")
async def reed_rabbit_message(
    broker_service: Annotated[BrokerService, Depends(get_broker_service)],
    queue_name: str,  # todo надо сделать модель
    timeout: int = 1  # todo надо сделать модель
):
    try:
        return await broker_service.get_single_message(queue_name, timeout)
    except QueueEmptyException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "error": "Message no found with this name"}
        )
    except MessageConsumeException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "error": "Ошибка при поиске сообщения"}
        )