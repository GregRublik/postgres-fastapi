import pytest
from httpx import AsyncClient, ASGITransport
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

# @pytest.mark.asyncio
# async def test_api():
#     async with AsyncClient(
#         transport=ASGITransport(app),
#         base_url='http://test'
#     ) as ac:
#         response = await ac.get("/invalid_url")
#         assert response.status_code == 404
#         response = await ac.get("/")
#         assert response.status_code == 200

def test_auth_register():
    response = client.post("/register")
    assert response.status_code == 200

def test_auth_login():
    response = client.post("/login")
    assert response.status_code == 200

def test_auth_logout():
    response = client.get("/logout")
    assert response.status_code == 200