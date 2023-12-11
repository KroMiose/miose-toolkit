from typing import Dict, Optional, Union

import aiohttp
import requests

try:
    import ujson as json
except ImportError:
    import json


class MFetch:
    """请求类"""

    @classmethod
    def fetch(
        cls,
        url,
        method: str = "get",
        params: Optional[Dict] = None,
        data: Union[str, Dict] = "{}",
        headers: Optional[Dict] = None,
        proxy_server: str = "",
        timeout: int = 60,
    ) -> str:
        """发起请求"""

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if isinstance(data, dict):
            data = json.dumps(data)

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
        return resp.text

    @classmethod
    async def async_fetch(
        cls,
        url,
        method: str = "get",
        params: Optional[Dict] = None,
        data: Union[str, Dict] = "{}",
        headers: Optional[Dict] = None,
        proxy_server: str = "",
        timeout: int = 60,
    ) -> str:
        """发起异步请求"""

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if isinstance(data, dict):
            data = json.dumps(data)

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
                return await resp.text()
