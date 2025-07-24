from fastapi import APIRouter
from fastapi.params import Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database.crud.ai_response import AIResponseService
from database.schemas.ai_response import AIResponseCreate, AIResponseRead, AIResponseUpdate

ai_response_router = APIRouter()


@ai_response_router.post("", response_model=AIResponseRead)
async def create_ai_response(db: AsyncSession = Depends(get_db),
                             data: AIResponseCreate = Body(...)) -> AIResponseRead:
    service = AIResponseService(db)
    return AIResponseRead.model_validate(await service.create(data))

@ai_response_router.put("/{ai_response_id}", response_model=AIResponseRead)
async def update_ai_response(ai_response_id: int, db: AsyncSession = Depends(get_db),
                             data: AIResponseUpdate = Body(...)) -> AIResponseRead:
    service = AIResponseService(db)
    return AIResponseRead.model_validate(await service.update(ai_response_id, data))

@ai_response_router.get("/{ai_response_id}", response_model=AIResponseRead)
async def get_ai_response(ai_response_id: int, db: AsyncSession = Depends(get_db)) -> AIResponseRead:
    service = AIResponseService(db)
    print(ai_response_id)
    return AIResponseRead.model_validate(await service.get(ai_response_id))