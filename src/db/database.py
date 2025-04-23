from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, Session

from fastapi import Depends
from config import settings
from typing import Annotated

Base = declarative_base()

engine = create_async_engine(
    url=settings.db.dsn_asyncpg,
    pool_size=5,
    max_overflow=10
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

def get_session():
    with async_session_maker() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
