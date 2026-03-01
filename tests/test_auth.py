import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "wronguser@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "incorrectos" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Inventory SaaS API" in response.json()["message"]
