from typing import Any, Dict, List, Optional, Union

import aiohttp
import requests

from .fetch import async_fetch, fetch, parse_cookies

try:
    import ujson as json  # type: ignore
except ImportError:
    import json


import json


class Response:
    """响应对象"""

    def __init__(
        self,
        text: str,
        status_code: int,
        raw_resp: requests.Response,
    ):
        self.text: str = text
        self.status_code: int = status_code
        self._raw_resp: requests.Response = raw_resp

    @property
    def raw_resp(self) -> requests.Response:
        """原始响应对象"""
        return self._raw_resp

    def __str__(self) -> str:
        return f"Response(status_code={self.status_code}, content={self.text})"

    def json(self) -> Any:
        return json.loads(self.text)


class AioResponse(Response):
    """异步响应对象"""

    def __init__(
        self,
        text: str,
        status_code: int,
        raw_resp: aiohttp.ClientResponse,
    ):
        self.text: str = text
        self.status_code: int = status_code
        self._raw_resp: aiohttp.ClientResponse = raw_resp

    @property
    def raw_resp(self) -> aiohttp.ClientResponse:
        """原始响应对象"""
        return self._raw_resp


class Mxios:
    def __init__(
        self,
        base_url: str = "",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
    ):
        self.base_url: str = base_url[:-1] if base_url.endswith("/") else base_url
        self.headers: Dict[str, str] = headers or {}
        self.cookies: Dict[str, str] = cookies or {}
        self.proxy_server: str = proxy_server
        self.timeout: int = timeout

    def fetch(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[Dict[str, str], str]] = None,
        data: Union[str, Dict, List] = "",
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> Response:
        """发起同步请求

        Args:
            url (str): 请求地址
            params (Optional[Dict[str, str]], optional): 请求参数. Defaults to None.
            headers (Optional[Dict[str, str]], optional): 请求头. Defaults to None.
            cookies (Optional[Dict[str, str]], optional): 请求cookie. Defaults to None.
            data (Union[str, Dict, List], optional): 请求体. Defaults to "{}".
            proxy_server (str, optional): 代理服务器. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            ssl_verify (bool, optional): 是否验证ssl. Defaults to True.
            allow_redirects (bool, optional): 是否允许重定向. Defaults to True.
        Returns:
            Response: 返回响应对象
        """

        headers = headers or {}
        headers = {**self.headers, **headers}

        if isinstance(cookies, str):
            cookies = parse_cookies(cookies)
        cookies = cookies or {}
        cookies = {**self.cookies, **cookies}

        params = params or {}

        if isinstance(data, (dict, list)):
            data = json.dumps(data)

        if not (url.startswith(("http://", "https://"))):
            url = self.base_url + url

        resp_status_code, resp_text, raw_resp = fetch(
            url=url,
            method=method,
            params=params,
            data=data,
            headers=headers,
            proxy_server=self.proxy_server or proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

        return Response(text=resp_text, status_code=resp_status_code, raw_resp=raw_resp)

    async def async_fetch(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Union[Dict[str, str], str]] = None,
        data: Union[str, Dict, List] = "",
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> AioResponse:
        """发起异步请求

        Args:
            url (str): 请求地址
            params (Optional[Dict[str, str]], optional): 请求参数. Defaults to None.
            headers (Optional[Dict[str, str]], optional): 请求头. Defaults to None.
            cookies (Optional[Dict[str, str]], optional): 请求cookie. Defaults to None.
            data (Union[str, Dict, List], optional): 请求体. Defaults to "{}".
            proxy_server (str, optional): 代理服务器. Defaults to "".
            timeout (int, optional): 超时时间. Defaults to 60.
            ssl_verify (bool, optional): 是否验证ssl. Defaults to True.
            allow_redirects (bool, optional): 是否允许重定向. Defaults to True.
        Returns:
            AioResponse: 返回响应对象
        """

        headers = headers or {}
        headers = {**self.headers, **headers}

        if isinstance(cookies, str):
            cookies = parse_cookies(cookies)
        cookies = cookies or {}
        cookies = {**self.cookies, **cookies}

        params = params or {}

        if isinstance(data, (dict, list)):
            data = json.dumps(data)

        if not (url.startswith(("http://", "https://"))):
            url = self.base_url + url

        resp_status_code, resp_text, raw_resp = await async_fetch(
            url=url,
            method=method,
            params=params,
            data=data,
            headers=headers,
            proxy_server=self.proxy_server or proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

        return AioResponse(
            text=resp_text,
            status_code=resp_status_code,
            raw_resp=raw_resp,
        )

    def get(
        self,
        url,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> Response:
        return self.fetch(
            method="get",
            url=url,
            params=params,
            headers=headers,
            proxy_server=proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

    def post(
        self,
        url,
        data: Union[str, Dict, List] = "",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> Response:
        return self.fetch(
            method="post",
            url=url,
            data=data,
            headers=headers,
            cookies=cookies,
            proxy_server=proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

    def put(
        self,
        url,
        params: Optional[Dict[str, str]] = None,
        data: Union[str, Dict, List] = "",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> Response:
        return self.fetch(
            method="put",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            proxy_server=proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

    def delete(
        self,
        url,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> Response:
        return self.fetch(
            method="delete",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            proxy_server=proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

    async def async_get(
        self,
        url,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> AioResponse:
        return await self.async_fetch(
            method="get",
            url=url,
            params=params,
            headers=headers,
            proxy_server=proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

    async def async_post(
        self,
        url,
        data: Union[str, Dict, List] = "",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> AioResponse:
        return await self.async_fetch(
            method="post",
            url=url,
            data=data,
            headers=headers,
            cookies=cookies,
            proxy_server=proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

    async def async_put(
        self,
        url,
        params: Optional[Dict[str, str]] = None,
        data: Union[str, Dict, List] = "",
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> AioResponse:
        return await self.async_fetch(
            method="put",
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            proxy_server=proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )

    async def async_delete(
        self,
        url,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        proxy_server: str = "",
        timeout: int = 60,
        ssl_verify: bool = True,
        allow_redirects=True,
    ) -> AioResponse:
        return await self.async_fetch(
            method="delete",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            proxy_server=proxy_server,
            timeout=timeout,
            ssl_verify=ssl_verify,
            allow_redirects=allow_redirects,
        )
