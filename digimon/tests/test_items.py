from httpx import AsyncClient
from digimon import models
import pytest


@pytest.mark.asyncio
async def test_no_permission_create_items(
    client: AsyncClient, merchant_user1: models.DBMerchant
):
    payload = {
        "name": "item1",
        "price": 10.5,
        "merchant_id": merchant_user1.id,
        "user_id": 1
    }
    response = await client.post("/items", json=payload)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_items(client: AsyncClient, token_user1: models.Token, merchant_user1: models.DBMerchant):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "name": "item1",
        "price": 10.5,
        "merchant_id": merchant_user1.id,
        "user_id": token_user1.user_id
    }
    response = await client.post("/items", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["merchant_id"] == payload["merchant_id"]
    assert data["id"] > 0


@pytest.mark.asyncio
async def test_update_items(client: AsyncClient, token_user1: models.Token, item_user1: models.DBItem):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}

    payload = {"name": "updated item name", "price": 12.5}
    response = await client.put(
        f"/items/{item_user1.id}", json=payload, headers=headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["id"] == item_user1.id


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient, token_user1: models.Token, item_user1: models.DBItem):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}

    response = await client.delete(f"/items/{item_user1.id}", headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert "success" in data["message"]


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/items", headers=headers)

    data = response.json()
    assert response.status_code == 200
    assert len(data["items"]) > 0
