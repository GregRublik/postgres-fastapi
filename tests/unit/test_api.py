import pytest


@pytest.mark.asyncio
async def test_auth_register(client):
    response = await client.post(
        "/register",
        json={
            "username": "admin",
            "email": "user15@example.com",
            "password": "asdasdfasdf",
        },
    )
    print(response.json())
    assert response.status_code in (200, 409)


@pytest.mark.asyncio
async def test_auth_login(client):
    response = await client.post(  # Работает напрямую с клиентом
        "/login",
        json={
            "email": "user15@example.com",
            "password": "asdasdfasdf",
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_auth_logout(client):
    response = await client.post("/logout")
    print(response.json())
    assert response.status_code == 200
