import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.telegram_account import TelegramAccountService
from database.schemas.telegram_account import TelegramAccountCreate


@pytest.mark.asyncio
async def test_create_account(client: AsyncClient, db: AsyncSession):
    data = TelegramAccountCreate(connection_id="fhue998fh9iodwusjhf9822", user_id=348573490, username="test_user")
    response = await client.post("/account", json=data.model_dump())
    assert response.status_code == 200
    assert response.json()["is_active"] is True

@pytest.mark.asyncio
async def test_get_account_by_connection(client: AsyncClient, db: AsyncSession):
    account_service = TelegramAccountService(db)
    data = TelegramAccountCreate(connection_id="fhue998fh9iodwusjhf9823", user_id=34857348, username="test_user")
    obj = await account_service.create(data)


    response = await client.get(f"/account/connection/{obj.connection_id}")
    assert response.status_code == 200
    assert response.json()["connection_id"] == data.connection_id

    response = await client.get(f"/account/connection/unexisting_connection_id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_account(client: AsyncClient, db: AsyncSession):
    account_service = TelegramAccountService(db)
    data = TelegramAccountCreate(connection_id="update_test_conn_id", user_id=123456, username="update_user")
    obj = await account_service.create(data)
    update_data = {"user_id": obj.user_id, "username": "updated_username"}
    response = await client.put(f"/account/user/{obj.user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["username"] == "updated_username"

@pytest.mark.asyncio
async def test_control_active(client: AsyncClient, db: AsyncSession):
    account_service = TelegramAccountService(db)
    data = TelegramAccountCreate(connection_id="active_test_conn_id", user_id=654321, username="active_user")
    obj = await account_service.create(data)
    response = await client.put(f"/account/user/{obj.user_id}/active", json={"is_active": False})
    assert response.status_code == 200
    assert response.json()["is_active"] is False
    response = await client.put(f"/account/user/{obj.user_id}/active", json={"is_active": True})
    assert response.status_code == 200
    assert response.json()["is_active"] is True


