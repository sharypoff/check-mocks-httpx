import httpx
import pytest
import pytest_asyncio
from pytest_httpx import HTTPXMock
from app.main import app

TEST_SERVER = "test_server"


@pytest_asyncio.fixture
async def non_mocked_hosts() -> list:
    return [TEST_SERVER]


@pytest.mark.asyncio
async def test_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://example.com/user",
        json={"id": 12, "name": "John", "age": 21},
        # content=b'{"name": "John", "age": 21}',
    )
    httpx_mock.add_response(
        method="POST",
        url="http://example1.com/group/23",
        json={"id": 23, "user_id": 12},
        # content=b'{"user_id": 12}',
    )
    async with httpx.AsyncClient(app=app, base_url=f"http://{TEST_SERVER}") as async_client:
        response = await async_client.post("/")
    assert response.status_code == 200
    assert response.json() == {
        'user': {'id': 12, 'name': 'John', 'age': 21},
        'group': {'id': 23, 'user_id': 12},
    }
