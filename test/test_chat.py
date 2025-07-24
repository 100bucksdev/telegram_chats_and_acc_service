from types import SimpleNamespace

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.chat import ChatService
from database.crud.message import MessageService
from database.crud.telegram_account import TelegramAccountService
from database.schemas.chat import ChatCreate
from database.schemas.message import MessageCreate
from database.schemas.telegram_account import TelegramAccountCreate

import itertools
_counter = itertools.count(123456)

@pytest_asyncio.fixture(scope="function")
async def seeded_data(db: AsyncSession) -> SimpleNamespace:
    account_service = TelegramAccountService(db)
    uid = next(_counter)
    data = TelegramAccountCreate(connection_id=f"dkfwldkfjweoijwe-{uid}", user_id=uid, username="test_user")
    return SimpleNamespace(account=await account_service.create(data))


@pytest.mark.asyncio
async def test_create_chat(client: AsyncClient, db: AsyncSession, seeded_data):
    data = ChatCreate(chat_id=89, chat_with_user_id=562, account_id=seeded_data.account.id)
    response = await client.post(f"/account/user/{seeded_data.account.user_id}/chat", json=data.model_dump())
    assert response.status_code == 200
    assert response.json()["chat_id"] == 89
    assert response.json()["chat_with_user_id"] == 562
    assert response.json()["account_id"] == seeded_data.account.id

    response = await client.post(f"/account/user/{seeded_data.account.user_id}/chat", json=data.model_dump())
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_add_message_to_chat(client: AsyncClient, db: AsyncSession, seeded_data):
    data = {
        'message': 'test message',
        'sender': 'client',
        'chat_with_user_id': 2,
        'message_id': 1043
    }
    # create a new chat and add a message to it
    response = await client.post(f"/account/user/{seeded_data.account.user_id}/chat/{3255}/message", json=data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message_text"] == "test message"
    assert response.json()["sender"] == "client"
    assert response.json()["chat_id"] == 1
    assert response.json()["message_id"] == 1043

    # add a new message to exist chat
    data['message_id'] = 1044
    data['sender'] = 'staff'
    response = await client.post(f"/account/user/{seeded_data.account.user_id}/chat/{3255}/message", json=data)
    assert response.status_code == 200

    # add a new message by AI
    data['sender'] = 'ai'
    data['message_id'] = 1045
    response = await client.post(f"/account/user/{seeded_data.account.user_id}/chat/{3255}/message", json=data)
    assert response.status_code == 200

    # try to add a new message for the wrong account id

    response = await client.post(f"/account/user/{seeded_data.account.user_id + 1}/chat/{3256}/message", json=data)
    assert response.status_code == 404
    assert response.json()["detail"] == "account_not_found"

@pytest.mark.asyncio
async def test_get_last_messages_from_chat(client: AsyncClient, db: AsyncSession, seeded_data):
    chat_service = ChatService(db)
    data = ChatCreate(chat_id=5, chat_with_user_id=2, account_id=seeded_data.account.id)
    chat = await chat_service.create(data)


    message_service = MessageService(db)
    for i in range(1, 6):
        msg_data = MessageCreate(message_text=f'test message {i}', sender='client', message_id=i, chat_id=chat.id)
        await message_service.create(msg_data)


    response = await client.get(f"/account/user/{seeded_data.account.user_id}/chat/{chat.chat_id}/last-messages?count={i}")
    assert response.status_code == 200
    assert len(response.json()) == i





