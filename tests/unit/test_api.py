import pytest


@pytest.mark.asyncio
async def test_auth_register(async_client):
    response = await async_client.post(
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
async def test_auth_login(async_client):
    response = await async_client.post(
        "/login",
        json={
            "email": "user15@example.com",
            "password": "asdasdfasdf",
        },
    )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_auth_logout(async_client):
    response = await async_client.get(
        "/logout"
    )
    print(response.json())
    assert response.status_code == 200
