from typing import AsyncGenerator

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config import DEBUG, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

if DEBUG:
    SQLALCHEMY_DATABASE_URL = r'sqlite:///C:\Users\peyro\PycharmProjects\tg_chats_and_account_service\db.sqlite'
    SQLALCHEMY_ASYNC_DATABASE_URL = r"sqlite+aiosqlite:///C:\Users\peyro\PycharmProjects\tg_chats_and_account_service\db.sqlite"
else:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine_async: AsyncEngine = create_async_engine(SQLALCHEMY_ASYNC_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine_async,
    expire_on_commit=False,
    class_=AsyncSession,
)

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session