from typing import List, Any, Coroutine, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.base import BaseService
from database.models.telegram_account import TelegramAccount
from database.schemas.telegram_account import TelegramAccountCreate, TelegramAccountUpdate


class TelegramAccountService(BaseService[TelegramAccount, TelegramAccountCreate, TelegramAccountUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(TelegramAccount, session)

    async def get_active_accounts(self) -> Sequence[TelegramAccount]:
        result = await self.session.execute(
            select(TelegramAccount).where(TelegramAccount.is_active.is_(True), TelegramAccount.session_id.isnot(None))
        )
        return result.scalars().all()

    async def get_account_by_connection_id(self, connection_id: str) -> TelegramAccount:
        result = await self.session.execute(
            select(TelegramAccount).where(TelegramAccount.connection_id == connection_id)
        )
        return result.scalars().one_or_none()

    async def get_account_by_user_id(self, user_id: int) -> TelegramAccount:
        result = await self.session.execute(
            select(TelegramAccount).where(TelegramAccount.user_id == user_id)
        )
        return result.scalars().one_or_none()

    async def is_active(self, account_id: int, active: bool) -> TelegramAccount | None:
        account = await self.get(account_id)
        if account is None:
            return None
        account.is_active = active
        await self.session.commit()
        await self.session.refresh(account)
        return account



