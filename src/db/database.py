from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings
from functools import wraps


engine = create_async_engine(
    url=settings.db.dsn_asyncpg,
    pool_size=5,
    max_overflow=10
)

# AsyncSessionLocal = async_sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
#     class_=AsyncSession
# )

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# def session_manager(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         async with AsyncSessionLocal() as session:  # Открываем сессию
#             return await func(*args, session, **kwargs)  # Передаем сессию в функцию
#     return wrapper
