from datetime import datetime, UTC
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.models import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .ai_response import AIResponse

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_text: Mapped[str] = mapped_column(String, nullable=False)
    message_id: Mapped[int] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"))
    sender: Mapped[str] = mapped_column(String, nullable=False)
    is_processed: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    chat: Mapped["Chat"] = relationship(back_populates="messages")

    ai_response_as_question: Mapped[Optional["AIResponse"]] = relationship(
        "AIResponse",
        back_populates="question_message",
        foreign_keys="AIResponse.question_message_id",
        uselist=False,
    )
    ai_response_as_answer: Mapped[Optional["AIResponse"]] = relationship(
        "AIResponse",
        back_populates="answer_message",
        foreign_keys="AIResponse.answer_message_id",
        uselist=False,
    )

