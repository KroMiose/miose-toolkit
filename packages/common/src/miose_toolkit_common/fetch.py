from typing import Dict, Optional, Tuple, cast

import aiohttp
import requests


def stringfy_cookies(cookies: Dict) -> str:
    """将cookies转换为字符串"""
    return "; ".join([f"{k}={v}" for k, v in cookies.items()])


def parse_cookies(cookies: str) -> Dict:
    """将字符串转换为cookies"""
    return dict(item.split("=") for item in cookies.split(";"))


def fetch(
    url,
    method: str = "get",
    params: Optional[Dict] = None,
    data: str = "",
    headers: Optional[Dict] = None,
    cookies: Optional[Dict] = None,
    proxy_server: str = "",
    timeout: int = 60,
    ssl_verify: bool = True,
    allow_redirects=True,
) -> Tuple[int, str, requests.Response]:
    """发起同步请求

    Args:
        url (str): 请求地址
        method (str, optional): 请求方法. Defaults to "get".
        params (Optional[Dict], optional): 请求参数. Defaults to None.
        data (str, optional): 请求数据. Defaults to "".
        headers (Optional[Dict], optional): 请求头. Defaults to None.
        cookies (Optional[Dict], optional): 请求cookies. Defaults to None.
        proxy_server (str, optional): 代理服务器. Defaults to "".
        timeout (int, optional): 请求超时时间. Defaults to 60.
        ssl_verify (bool, optional): 是否验证ssl. Defaults to True.
        allow_redirects (bool, optional): 是否允许重定向. Defaults to True.
    Returns:
        Tuple[int, str, requests.Response]: [description]
        status_code: 状态码
        text: 响应文本
        raw_resp: 原始响应对象
    """

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

    resp: requests.Response = cast(
        requests.Response,
        getattr(requests, method.lower())(
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            proxies=proxies,
            timeout=timeout,
            verify=ssl_verify,
            allow_redirects=allow_redirects,
        ),
    )
    return resp.status_code, resp.text, resp


async def async_fetch(
    url,
    method: str = "get",
    params: Optional[Dict] = None,
    data: str = "",
    headers: Optional[Dict] = None,
    cookies: Optional[Dict] = None,
    proxy_server: str = "",
    timeout: int = 60,
    ssl_verify: bool = True,
    allow_redirects: bool = True,
) -> Tuple[int, str, aiohttp.ClientResponse]:
    if headers is None:
        headers = {}
    if cookies:
        headers["Cookie"] = stringfy_cookies(cookies)
    if params is None:
        params = {}

    # 使用 TCPConnector 来处理代理和SSL验证
    conn = aiohttp.TCPConnector(
        verify_ssl=ssl_verify,
    )

    # 创建 ClientSession 实例时指定 connector 和 headers
    async with aiohttp.ClientSession(
        connector=conn if proxy_server else None,
        headers=headers,
        timeout=aiohttp.ClientTimeout(total=timeout),
    ) as session, getattr(session, method.lower())(
        url,
        params=params,
        data=data,
        allow_redirects=allow_redirects,
        proxy=proxy_server if proxy_server else None,
        ssl=ssl_verify,
    ) as resp:
        resp = cast(aiohttp.ClientResponse, resp)
        return resp.status, await resp.text(), resp
