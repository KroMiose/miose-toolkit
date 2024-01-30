from typing import Dict, Optional, Tuple, Union

import aiohttp
import requests


def fetch(
    url,
    method: str = "get",
    params: Optional[Dict] = None,
    data: str = "",
    headers: Optional[Dict] = None,
    proxy_server: str = "",
    timeout: int = 60,
) -> Tuple[int, str]:
    """发起请求"""

    if headers is None:
        headers = {}
    if params is None:
        params = {}

    if proxy_server:
        proxies = {
            "http": f"http://{proxy_server}",
            "https": f"https://{proxy_server}",
        }
    else:
        proxies = None

    resp = getattr(requests, method)(
        url,
        params=params,
        data=data,
        headers=headers,
        proxies=proxies,
        timeout=timeout,
    )
    return resp.status_code, resp.text


async def async_fetch(
    url,
    method: str = "get",
    params: Optional[Dict] = None,
    data: str = "",
    headers: Optional[Dict] = None,
    proxy_server: str = "",
    timeout: int = 60,
) -> Tuple[int, str]:
    """发起异步请求"""

    if headers is None:
        headers = {}
    if params is None:
        params = {}

    async with aiohttp.ClientSession(headers=headers) as session:
        if proxy_server:
            conn = aiohttp.TCPConnector(limit=10, verify_ssl=False)
            session = aiohttp.ClientSession(connector=conn)
            session._default_headers.update(  # noqa: SLF001
                {"Proxy-Switch-Ip": "yes"},
            )
            session._default_headers.update(  # noqa: SLF001
                {"Proxy-Server": proxy_server},
            )
        async with getattr(session, method)(
            url,
            params=params,
            data=data,
            timeout=timeout,
        ) as resp:
            return resp.status, await resp.text()
