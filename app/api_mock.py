from typing import Any
import httpx
import json
from pytest_httpx import HTTPXMock


class APIMock:
    def __init__(self, httpx_mock: HTTPXMock):
        self.httpx_mock = httpx_mock

    async def request_mock(
            self,
            method: str,
            url: str,
            status_code: int = 200,
            request_for_check: Any = None,
            **kwargs,
    ):
        async def custom_response(request: httpx.Request) -> httpx.Response:
            response = httpx.Response(
                status_code,
                **kwargs,
            )
            if request_for_check:
                assert request_for_check == json.loads(request.content), \
                    f"{request_for_check} != {json.loads(request.content)}"
            return response
        self.httpx_mock.add_callback(custom_response, method=method, url=url)
