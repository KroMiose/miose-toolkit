from urllib.parse import quote, unquote


class MUrl:
    """url工具类"""

    @classmethod
    def get_url_domain(cls, url: str) -> str:
        """获取url的域名"""

        try:
            return url.split("//")[1].split("/")[0]
        except Exception:
            return ""

    @classmethod
    def get_url_path(cls, url: str) -> str:
        """获取url的路径"""

        path = url.split("//")[1].split("/", 1)  # Split only once
        if len(path) > 1:
            return "/" + path[1]
        return "/"

    @classmethod
    def get_url_params(cls, url: str, use_unquote: bool = True) -> dict:
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

    @classmethod
    def drop_url_anchor(cls, url: str) -> str:
        """去除url中的锚点"""

        if url.startswith("#"):
            return ""
        return url.split("#")[0]

    @classmethod
    def is_relative_url(cls, url: str) -> bool:
        """判断url是否为相对路径"""

        return url.startswith(("/", "#"))
