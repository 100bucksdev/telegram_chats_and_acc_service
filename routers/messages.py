from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.chat import ChatService
from database.crud.message import MessageService
from database.db.session import get_db
from database.schemas.message import MessageRead

message_router = APIRouter()

@message_router.get("/{chat_id}/get-unprocessed-messages", response_model=List[MessageRead])
async def get_messages(chat_id: int, db: AsyncSession = Depends(get_db))-> List[MessageRead]:
    chat_service = ChatService(db)
    chat = await chat_service.get_chat_by_chat_id(chat_id)
    service = MessageService(db)
    return [MessageRead.model_validate(message) for message in await service.get_unprocessed_messages(chat.id)]


