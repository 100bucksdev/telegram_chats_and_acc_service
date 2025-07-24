from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.chat import ChatService
from database.db.session import get_db

data_for_processing_router = APIRouter()

@data_for_processing_router.get("/get-chats-ids")
async def get_chats_ids(db: AsyncSession = Depends(get_db))-> List[int]:
    service = ChatService(db)
    chats_ids = await service.get_chats_ids_with_unprocessed_messages()
    return chats_ids

