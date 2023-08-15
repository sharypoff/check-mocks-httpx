import httpx
import pytest
import pytest_asyncio
from pytest_httpx import HTTPXMock
from app.main import app
from app.api_mock import APIMock

TEST_SERVER = "test_server"


@pytest_asyncio.fixture
async def non_mocked_hosts() -> list:
    return [TEST_SERVER]


@pytest_asyncio.fixture
async def requests_mock(httpx_mock: HTTPXMock):
    return APIMock(httpx_mock)


@pytest.mark.asyncio
async def test_with_requests_success(requests_mock):
    await requests_mock.request_mock(
        method="POST",
        url="http://example.com/user",
        json={"id": 12, "name": "John", "age": 21},
        request_for_check={"name": "John", "age": 21},
    )
    await requests_mock.request_mock(
        method="POST",
        url="http://example1.com/group/23",
        json={"id": 23, "user_id": 12},
        request_for_check={"user_id": 12},
    )
    async with httpx.AsyncClient(app=app, base_url=f"http://{TEST_SERVER}") as async_client:
        response = await async_client.post("/")
    assert response.status_code == 200
    assert response.json() == {
        'user': {'id': 12, 'name': 'John', 'age': 21},
        'group': {'id': 23, 'user_id': 12},
    }
