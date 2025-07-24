from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime


class MessageBase(BaseModel):
    message_text: str
    chat_id: int
    message_id: int
    sender: Literal['client', 'staff', 'ai']
    created_at: Optional[datetime] = None


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    message_text: Optional[str] = None
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    sender: Optional[Literal['client', 'stuff']] = None
    created_at: Optional[datetime] = None


class MessageRead(MessageBase):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
