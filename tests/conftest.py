import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)  # <-- correct way
    async with AsyncClient(
        transport=transport,
        base_url="http://localhost:8000"
    ) as ac:
        yield ac
