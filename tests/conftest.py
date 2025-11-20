import pytest
from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import event, Engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from httpx import AsyncClient

from core.models.base import Base

from core.database import get_session
from main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Включение каскадного удаления для sqlite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


test_engine = create_async_engine(
    TEST_DATABASE_URL,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncClient:
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def sample_question_data():
    return {"text": "What is Python?"}


@pytest.fixture
async def sample_answer_data():
    return {"text": "Python is a programming language", "user_id": "user-123"}
