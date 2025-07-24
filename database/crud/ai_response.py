from sqlalchemy.ext.asyncio import AsyncSession
from database.crud.base import BaseService
from database.models.ai_response import AIResponse
from database.schemas.ai_response import AIResponseUpdate, AIResponseCreate


class AIResponseService(BaseService[AIResponse, AIResponseCreate, AIResponseUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(AIResponse, session)





