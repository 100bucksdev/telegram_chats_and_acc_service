from typing import Any, AsyncGenerator
from types import SimpleNamespace

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import create_app
from database.crud.telegram_account import TelegramAccountService
from database.schemas.telegram_account import TelegramAccountCreate

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="session")
def app() -> FastAPI:
    return create_app()

@pytest_asyncio.fixture(scope="function")
async def async_engine():
    engine = create_async_engine(
        TEST_DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

@pytest_asyncio.fixture(autouse=True)
def no_commit(monkeypatch):
    async def _flush_only(self):
        await self.flush()
    monkeypatch.setattr(AsyncSession, "commit", _flush_only)

@pytest_asyncio.fixture(scope="function")
async def db(async_engine) -> AsyncGenerator[AsyncSession, Any]:
    async with async_engine.connect() as conn:
        trans = await conn.begin()
        async_session_factory = async_sessionmaker(bind=conn, expire_on_commit=False, class_=AsyncSession)
        async with async_session_factory() as session:
            await session.begin_nested()

            @event.listens_for(session.sync_session, "after_transaction_end")
            def _restart_savepoint(sess, trans_):
                if trans_.nested and not trans_._parent.nested:
                    sess.begin_nested()

            yield session
        await trans.rollback()

@pytest_asyncio.fixture()
async def client(app: FastAPI, db: AsyncSession) -> AsyncGenerator[AsyncClient, Any]:
    async def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
