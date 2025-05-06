from fastapi import Cookie, APIRouter, Request, WebSocket
from typing import Dict, Annotated
from config import templates

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


@main.get("rabbit_test/")
async def index(

):
    pass
