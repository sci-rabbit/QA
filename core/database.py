from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import settings

engine = create_async_engine(
    url=settings.db.url,
)


async def dispose() -> None:
    await engine.dispose()


async_session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session



