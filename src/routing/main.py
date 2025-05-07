from fastapi import Cookie, APIRouter, Request, WebSocket, Depends
from depends import get_broker_service
from typing import Dict, Annotated
from config import templates
from services.broker import BrokerService

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
):
    return await broker_service.get_single_message("first_message")
