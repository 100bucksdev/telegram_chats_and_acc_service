from datetime import datetime, UTC
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.models import Base
if TYPE_CHECKING:
    from .message import Message
    from .telegram_account import TelegramAccount


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(nullable=False)

    chat_with_user_id: Mapped[int] = mapped_column(nullable=False)

    account_id: Mapped[int] = mapped_column(ForeignKey("telegram_account.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    account: Mapped['TelegramAccount'] = relationship(back_populates="chats")
    messages: Mapped[List['Message']] = relationship(back_populates="chat")