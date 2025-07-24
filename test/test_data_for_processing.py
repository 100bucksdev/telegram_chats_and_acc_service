import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.chat import ChatService
from database.crud.message import MessageService
from database.schemas.chat import ChatCreate
from database.schemas.message import MessageCreate


@pytest.mark.asyncio
async def test_data_for_processing(client: AsyncClient, db: AsyncSession):
    chat_service = ChatService(db)
    chat_ids = []
    for i in range(1, 10):
        chat_data = ChatCreate(chat_id=i+1, chat_with_user_id=i+ 2, account_id=i + 3)
        chat = await chat_service.create(chat_data)
        chat_ids.append(chat.id)

    message_service = MessageService(db)
    for chat_id in chat_ids:
        message = MessageCreate(message_text="test message", sender="client", message_id=1043, chat_id=chat_id)
        await message_service.create(message)
    response = await client.get("/data-for-processing/get-chats-ids")
    assert response.status_code == 200
    assert len(response.json()) == 9