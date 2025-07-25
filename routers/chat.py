from typing import Literal, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.chat import ChatService
from database.crud.message import MessageService
from database.crud.telegram_account import TelegramAccountService
from database.db.session import get_db
from database.schemas.chat import ChatCreate, ChatRead
from database.schemas.message import MessageCreate, MessageRead
from schemas.message import MessageIn

chat_router = APIRouter()

@chat_router.post("", response_model=ChatRead)
async def add_chat_if_not_exist(user_id: int, chat_id: int = Body(...),chat_with_user_id:int = Body(...), db: AsyncSession = Depends(get_db))->ChatRead:
        account_service = TelegramAccountService(db)
        account = await account_service.get_account_by_user_id(user_id)

        chat_service = ChatService(db)
        if await chat_service.get_chat_by_chat_id(chat_id):
            raise HTTPException(
                status_code=400, detail='chat_already_exists')

        chat = await chat_service.get_chat_by_chat_id(chat_id)
        if not chat:
            chat = await chat_service.create(ChatCreate(chat_id=chat_id, account_id=account.id,
                                                        chat_with_user_id=chat_with_user_id))
        return ChatRead.model_validate(chat)

@chat_router.post("/{chat_id}/message", response_model=MessageRead)
async def add_message(user_id: int, chat_id: int, payload: MessageIn, db: AsyncSession = Depends(get_db)) -> MessageRead:
    account_service = TelegramAccountService(db)
    chat_service = ChatService(db)
    message_service = MessageService(db)

    account = await account_service.get_account_by_user_id(payload.user_id)
    if not account:
        raise HTTPException(status_code=404, detail="account_not_found")

    chat = await chat_service.get_chat_by_chat_id(chat_id)
    if not chat:
        chat = await chat_service.create(ChatCreate(chat_id=chat_id, account_id=account.id, chat_with_user_id=payload.chat_with_user_id))

    created = await message_service.create(MessageCreate(message_text=payload.message, chat_id=chat.id, sender=payload.sender, message_id=payload.message_id))

    return MessageRead.model_validate(created)

@chat_router.get('/{chat_id}/last-messages', response_model=List[MessageRead])
async def get_last_five_messages(chat_id: int, count:int = Query(5), db: AsyncSession = Depends(get_db)) -> List[MessageRead]:
    message_service = MessageService(db)
    chat_service = ChatService(db)
    chat = await chat_service.get_chat_by_chat_id(chat_id)
    if not chat:
        raise HTTPException(
            status_code=404, detail='chat_not_found')
    result = await message_service.get_last_messages_from_chat(chat.id, count)
    return [MessageRead.model_validate(message) for message in result]















