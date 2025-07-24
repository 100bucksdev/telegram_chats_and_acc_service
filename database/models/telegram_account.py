from datetime import datetime, UTC
from typing import List, TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.models import Base
if TYPE_CHECKING:
    from .chat import Chat


class TelegramAccount(Base):
    __tablename__ = "telegram_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)

    connection_id: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    chats: Mapped[List['Chat']] = relationship(back_populates="account", cascade="all, delete-orphan")

