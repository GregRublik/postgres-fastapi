import pytest
from httpx import AsyncClient, ASGITransport
import sys
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator, Any

sys.path.append("src/")

from db.database import get_db_session
from config import settings
from app import app


async def _get_test_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        test_engine = create_async_engine(
            settings.db_test.dsn_asyncpg, future=True, echo=True
        )
        test_async_session = async_sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db_session] = _get_test_db
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as ac:
        yield ac
