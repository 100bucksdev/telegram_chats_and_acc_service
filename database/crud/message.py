from sqlalchemy import update, select, Sequence, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.base import BaseService
from database.models.message import Message
from database.schemas.message import MessageCreate, MessageUpdate


class MessageService(BaseService[Message, MessageCreate, MessageUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Message, session)

    async def make_messages_from_chat_processed(self, chat_id: int):
        stmt = (
            update(Message)
            .where(Message.chat_id == chat_id)
            .values(is_processed=True)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_unprocessed_messages(self, chat_id: int)-> Sequence[Message]:
        print(chat_id)
        stmt = select(Message).where(
            Message.chat_id == chat_id,
            or_(
                Message.is_processed == False,
                Message.is_processed.is_(None)
            )
        )
        result = await self.session.execute(stmt)
        result =  result.scalars().all()
        print(result)
        return result

    async def get_last_messages_from_chat(self, chat_id: int, count: int = 10)-> Sequence[Message]:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(count)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

