from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AIResponseBase(BaseModel):
    ai_response: str
    question_message_id: int
    answer_message_id: Optional[int] = None
    created_at: Optional[datetime] = None

class AIResponseCreate(AIResponseBase):
    pass

class AIResponseUpdate(BaseModel):
    ai_response: Optional[str] = None
    question_message_id: Optional[int] = None
    answer_message_id: Optional[int] = None
    created_at: Optional[datetime] = None

class AIResponseRead(AIResponseBase):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
