from typing import Dict, Optional, Union

from .fetch import async_fetch, fetch

try:
    import ujson as json
except ImportError:
    import json


class Response:
    def __init__(self, text: str, status_code: int):
        self.text = text
        self.status_code = status_code

    def __str__(self):
        return f"Response(text={self.text}, status_code={self.status_code})"

    def __repr__(self):
        return self.__str__()

    def json(self):
        return json.loads(self.text)


class Mxios:
    def __init__(
        self,
        base_url: str = "",
        headers: Optional[Dict] = None,
        proxy_server: str = "",
        timeout: int = 60,
    ):
        self.base_url = base_url if not base_url.endswith("/") else base_url[:-1]
        self.headers = headers or {}
        self.proxy_server = proxy_server
        self.timeout = timeout

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        data: Union[str, Dict] = "{}",
        proxy_server: str = "",
        timeout: int = 60,
    ) -> Response:
        """发起请求"""

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if isinstance(data, (dict, list)):
            data = json.dumps(data)

        if not (url.startswith(("http://", "https://"))):
            url = self.base_url + url

        headers = {**self.headers, **headers}

        resp_status_code, resp_text = fetch(
            url=url,
            method=method,
            params=params,
            data=data,
            headers=headers,
            proxy_server=self.proxy_server or proxy_server,
            timeout=timeout,
        )

        return Response(resp_text, resp_status_code)

    async def async_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        data: Union[str, Dict] = "{}",
        proxy_server: str = "",
        timeout: int = 60,
    ) -> Response:
        """发起异步请求"""

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if isinstance(data, (dict, list)):
            data = json.dumps(data)

        if not (url.startswith(("http://", "https://"))):
            url = self.base_url + url

        headers = {**self.headers, **headers}

        resp_status_code, resp_text = await async_fetch(
            url=url,
            method=method,
            params=params,
            data=data,
            headers=headers,
            proxy_server=self.proxy_server or proxy_server,
            timeout=timeout,
        )

        return Response(resp_text, resp_status_code)

    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, proxy_server: str = "", timeout: int = 60) -> Response:
        return self.request(method="get", url=url, params=params, headers=headers, proxy_server=proxy_server, timeout=timeout)

    async def async_get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, proxy_server: str = "", timeout: int = 60) -> Response:
        return await self.async_request(method="get", url=url, params=params, headers=headers, proxy_server=proxy_server, timeout=timeout)
    
    def post(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, data: Union[str, Dict] = "{}", proxy_server: str = "", timeout: int = 60) -> Response:
        return self.request(method="post", url=url, params=params, headers=headers, data=data, proxy_server=proxy_server, timeout=timeout)
    
    async def async_post(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, data: Union[str, Dict] = "{}", proxy_server: str = "", timeout: int = 60) -> Response:
        return await self.async_request(method="post", url=url, params=params, headers=headers, data=data, proxy_server=proxy_server, timeout=timeout)
    
    def put(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, data: Union[str, Dict] = "{}", proxy_server: str = "", timeout: int = 60) -> Response:
        return self.request(method="put", url=url, params=params, headers=headers, data=data, proxy_server=proxy_server, timeout=timeout)
    
    async def async_put(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, data: Union[str, Dict] = "{}", proxy_server: str = "", timeout: int = 60) -> Response:
        return await self.async_request(method="put", url=url, params=params, headers=headers, data=data, proxy_server=proxy_server, timeout=timeout)
    
    def delete(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, data: Union[str, Dict] = "{}", proxy_server: str = "", timeout: int = 60) -> Response:
        return self.request(method="delete", url=url, params=params, headers=headers, data=data, proxy_server=proxy_server, timeout=timeout)
    
    async def async_delete(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, data: Union[str, Dict] = "{}", proxy_server: str = "", timeout: int = 60) -> Response:
        return await self.async_request(method="delete", url=url, params=params, headers=headers, data=data, proxy_server=proxy_server, timeout=timeout)
    
    def patch(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, data: Union[str, Dict] = "{}", proxy_server: str = "", timeout: int = 60) -> Response:
        return self.request(method="patch", url=url, params=params, headers=headers, data=data, proxy_server=proxy_server, timeout=timeout)
    
    async def async_patch(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, data: Union[str, Dict] = "{}", proxy_server: str = "", timeout: int = 60) -> Response:
        return await self.async_request(method="patch", url=url, params=params, headers=headers, data=data, proxy_server=proxy_server, timeout=timeout)

