import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import logger, settings, session_manager
import sentry_sdk

from routing import main, chats, groups, messages, user_group_association, users

sentry_sdk.init(
    dsn=settings.sentry_url,
    send_default_pii=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(_apps: FastAPI):
    try:
        yield
    finally:
        await session_manager.close_session()

app = FastAPI(lifespan=lifespan)

# map(app.include_router,
#     [
#         # main.main,
#         chats.chats,
#         groups.groups,
#         messages.messages,
#         user_group_association.user_group_association,
#         users.users
#     ])
app.include_router(chats.chats)
app.include_router(groups.groups)
app.include_router(messages.messages)
app.include_router(user_group_association.user_group_association)
app.include_router(users.users)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


if __name__ == "__main__":
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=settings.app_port,
            log_config="src/logs/log_config.json",
            use_colors=True,
            log_level="info",
            loop="asyncio",
        )
    except Exception as e:
        logger.error(f"Error launch app: {e}")
