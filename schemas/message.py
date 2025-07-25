from typing import Literal

from pydantic import BaseModel


class MessageIn(BaseModel):
    message: str
    sender: Literal['client', 'staff', 'ai']
    chat_with_user_id: int
    message_id: int