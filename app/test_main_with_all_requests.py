import json

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
async def test_with_all_requests_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://example.com/user",
        json={"id": 12, "name": "John", "age": 21},
    )
    httpx_mock.add_response(
        method="POST",
        url="http://example1.com/group/23",
        json={"id": 23, "user_id": 12},
    )
    async with httpx.AsyncClient(app=app, base_url=f"http://{TEST_SERVER}") as async_client:
        response = await async_client.post("/")
    assert response.status_code == 200
    assert response.json() == {
        'user': {'id': 12, 'name': 'John', 'age': 21},
        'group': {'id': 23, 'user_id': 12},
    }
    expected_requests = [
        {"url": "http://example.com/user", "json": {"name": "John", "age": 21}},
        {"url": "http://example1.com/group/23", "json": {"user_id": 12}},
    ]
    for expecter_request, real_request in zip(expected_requests, httpx_mock.get_requests()):
        assert expecter_request["url"] == real_request.url
        assert expecter_request["json"] == json.loads(real_request.content)
