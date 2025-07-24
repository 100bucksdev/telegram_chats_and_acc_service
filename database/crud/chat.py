from typing import List, Any, Coroutine, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.base import BaseService
from database.models.chat import Chat
from database.models.message import Message
from database.schemas.chat import ChatCreate, ChatUpdate

class ChatService(BaseService[Chat, ChatCreate, ChatUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Chat, session)

    async def get_chat_by_chat_id(self, chat_id: int)-> Chat | None:
        result = await self.session.execute(
            select(Chat).where(Chat.chat_id == chat_id)
        )
        return result.scalar_one_or_none()

    async def get_chats_ids_with_unprocessed_messages(self) -> List[int]:
        stmt = (
            select(Chat.chat_id)
            .join(Message, Chat.id == Message.chat_id)
            .where(Message.is_processed.is_(False))
            .distinct()
        )
        result = await self.session.execute(stmt)
        return [row for row in result.scalars().all()]



