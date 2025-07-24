from datetime import datetime, UTC
from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.models import Base
if TYPE_CHECKING:
    from .message import Message


class AIResponse(Base):
    __tablename__ = "ai_response"

    id: Mapped[int] = mapped_column(primary_key=True)
    ai_response: Mapped[str] = mapped_column(String, nullable=False)

    question_message_id: Mapped[int] = mapped_column(
        ForeignKey("message.id"),
        nullable=False,
        unique=True,
    )
    answer_message_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("message.id"),
        nullable=True,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    question_message: Mapped["Message"] = relationship(
        "Message",
        foreign_keys=[question_message_id],
        back_populates="ai_response_as_question",
        uselist=False,
    )
    answer_message: Mapped[Optional["Message"]] = relationship(
        "Message",
        foreign_keys=[answer_message_id],
        back_populates="ai_response_as_answer",
        uselist=False,
    )