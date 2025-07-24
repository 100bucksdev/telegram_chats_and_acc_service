from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChatBase(BaseModel):
    chat_id: int
    chat_with_user_id: int
    account_id: int
    created_at: Optional[datetime] = None


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    chat_id: Optional[int] = None
    chat_with_user_id: Optional[int] = None
    account_id: Optional[int] = None
    created_at: Optional[datetime] = None


class ChatRead(ChatBase):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)