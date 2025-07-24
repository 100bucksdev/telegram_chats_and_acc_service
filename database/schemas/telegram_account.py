from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TelegramAccountBase(BaseModel):
    username: Optional[str] = None
    connection_id: str
    is_active: Optional[bool] = True
    user_id: int
    created_at: Optional[datetime] = None


class TelegramAccountCreate(TelegramAccountBase):
    pass


class TelegramAccountUpdate(BaseModel):
    username: Optional[str] = None
    is_active: Optional[bool] = False
    connection_id: Optional[str] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None


class TelegramAccountRead(TelegramAccountBase):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)