from urllib.parse import quote, unquote, urlparse


def get_url_domain(url: str) -> str:
    """获取url的域名"""

    try:
        return url.split("//")[1].split("/")[0]
    except Exception:
        return ""


def get_url_path(url: str) -> str:
    """获取url的路径"""

    path = url.split("//")[1].split("/", 1)  # Split only once
    if len(path) > 1:
        return "/" + path[1]
    return "/"


def get_url_params(url: str, use_unquote: bool = True) -> dict:
    """获取url的参数"""

    try:
        params = {}
        for param in url.split("?")[1].split("&"):
            k, v = param.split("=")
            params[k] = v if not use_unquote else unquote(v)
    except Exception:
        return {}
    else:
        return params


def drop_url_anchor(url: str) -> str:
    """去除url中的锚点"""

    if url.startswith("#"):
        return ""
    return url.split("#")[0]


def is_relative_url(url: str) -> bool:
    """判断url是否为相对路径"""

    return url.startswith(("/", "#"))


def trans_str_to_url(s: str) -> str:
    """将字符串转换为url"""

    return quote(s, safe="")


def gen_proxy_url(
    proxy_host: str,
    proxy_port: int,
    proxy_username: str = "",
    proxy_password: str = "",
    protocol: str = "http",
) -> str:
    return urlparse(
        f"{protocol}//{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
    ).geturl()
