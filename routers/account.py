from fastapi import HTTPException
from typing import List

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession



from database.crud.telegram_account import TelegramAccountService
from database.db.session import get_db
from database.schemas.telegram_account import TelegramAccountRead, TelegramAccountCreate, TelegramAccountUpdate

account_router = APIRouter()


@account_router.post('', response_model=TelegramAccountRead)
async def connect_account(data: TelegramAccountCreate = Body(...), db: AsyncSession = Depends(get_db)):
    acc_srv = TelegramAccountService(db)
    account = await acc_srv.get_account_by_connection_id(data.connection_id)
    if account is None:
        account = await acc_srv.create(data)
    else:
        raise HTTPException(status_code=400, detail={"message": "account_already_connected"})
    return TelegramAccountRead.model_validate(account)

@account_router.get('/connection/{connection_id}', response_model=TelegramAccountRead)
async def get_account_by_connection_id(connection_id: str, db: AsyncSession = Depends(get_db)):
    acc_srv = TelegramAccountService(db)
    account = await acc_srv.get_account_by_connection_id(connection_id)
    if account is None:
        raise HTTPException(status_code=404, detail={"message": "account_not_found"})
    return TelegramAccountRead.model_validate(account)

@account_router.get('/user/{user_id}', response_model=TelegramAccountRead)
async def get_account_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    acc_srv = TelegramAccountService(db)
    account = await acc_srv.get_account_by_user_id(user_id)
    if account is None:
        raise HTTPException(status_code=404, detail={"message": "account_not_found"})
    return TelegramAccountRead.model_validate(account)

@account_router.put('/user/{user_id}', response_model=TelegramAccountRead)
async def update_account(data: TelegramAccountUpdate = Body(...), db: AsyncSession = Depends(get_db)):
    acc_srv = TelegramAccountService(db)
    account = await acc_srv.get_account_by_user_id(data.user_id)
    if account is None:
        raise HTTPException(status_code=404, detail={"message": "account_not_found"})
    updated_account = await acc_srv.update(account.id, data)
    print(updated_account)
    return TelegramAccountRead.model_validate(updated_account)

@account_router.put('/user/{user_id}/active', response_model=TelegramAccountRead)
async def control_active(user_id: int, is_active: bool = Body(..., embed=True), db: AsyncSession = Depends(get_db)):
    acc_srv = TelegramAccountService(db)
    account = await acc_srv.get_account_by_user_id(user_id)
    account = await acc_srv.is_active(account.id, is_active)
    if account is None:
        raise HTTPException(status_code=404, detail={"message": "account_not_found"})
    return TelegramAccountRead.model_validate(account)
