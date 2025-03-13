from fastapi import APIRouter, Request
from authx import AuthX, AuthXConfig
from config import templates


auth = APIRouter()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


@auth.get("/login")
async def login(
        request: Request
):
    return templates.TemplateResponse(
        request,
        name="auth.html",
        context={}
    )


@auth.get("/register")
async def register(
        user:
):
    pass
