import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.ai_response import AIResponseService
from database.crud.chat import ChatService
from database.crud.message import MessageService
from database.schemas.ai_response import AIResponseCreate, AIResponseUpdate
from database.schemas.chat import ChatCreate
from database.schemas.message import MessageCreate

@pytest.mark.asyncio
async def test_create_and_update_ai_response(client: AsyncClient, db: AsyncSession):
    # 1. Create chat
    chat_service = ChatService(db)
    chat_data = ChatCreate(chat_id=1, chat_with_user_id=2, account_id=3)
    chat = await chat_service.create(chat_data)

    # 2. Create question message in chat
    message_service = MessageService(db)
    question_msg_data = MessageCreate(
        message_text="What is AI?",
        chat_id=chat.id,
        message_id=101,
        sender="client"
    )
    question_msg = await message_service.create(question_msg_data)

    # 3. Create AI response linked to question message
    ai_response_data = AIResponseCreate(
        ai_response="AI stands for Artificial Intelligence.",
        question_message_id=question_msg.id
    )
    response = await client.post("/ai-response", json=ai_response_data.model_dump())
    assert response.status_code == 200
    ai_response_id = response.json()["id"]
    assert response.json()["ai_response"] == "AI stands for Artificial Intelligence."
    assert response.json()["question_message_id"] == question_msg.id
    assert response.json()["answer_message_id"] is None

    # 4. Create answer message from AI
    answer_msg_data = MessageCreate(
        message_text="AI stands for Artificial Intelligence.",
        chat_id=chat.id,
        message_id=102,
        sender="ai"
    )
    answer_msg = await message_service.create(answer_msg_data)

    # 5. Update AI response with answer message id
    update_data = AIResponseUpdate(answer_message_id=answer_msg.id)
    update_response = await client.put(f"/ai-response/{ai_response_id}", json=update_data.model_dump())
    assert update_response.status_code == 200
    assert update_response.json()["answer_message_id"] == answer_msg.id

@pytest.mark.asyncio
async def test_get_ai_response(client: AsyncClient, db: AsyncSession):
    # Setup: create chat, message, and AI response
    chat_service = ChatService(db)
    chat_data = ChatCreate(chat_id=2, chat_with_user_id=3, account_id=4)
    chat = await chat_service.create(chat_data)


    message_service = MessageService(db)
    question_msg_data = MessageCreate(
        message_text="What is ML?",
        chat_id=chat.id,
        message_id=201,
        sender="client"
    )
    question_msg = await message_service.create(question_msg_data)

    ai_response_service = AIResponseService(db)
    ai_response_data = AIResponseCreate(
        ai_response="ML stands for Machine Learning.",
        question_message_id=question_msg.id
    )
    ai_response = await ai_response_service.create(ai_response_data)

    response = await client.get(f"/ai-response/{ai_response.id}")

    assert response.status_code == 200
    assert response.json()["id"] == ai_response.id
    assert response.json()["ai_response"] == "ML stands for Machine Learning."
    assert response.json()["question_message_id"] == question_msg.id
