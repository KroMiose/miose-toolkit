from pathlib import Path
from typing import Any, Dict

try:
    import ujson as json
except ImportError:
    import json


class MFile:
    @classmethod
    def ensure_path(cls, path: str):
        """确保路径目录存在

        :param path: 路径
        :param use_parent: 是否使用父目录
        """

        Path(path).mkdir(parents=True, exist_ok=True)
        return path

    @classmethod
    def ensure_dir(cls, root: str):
        """确保路径根目录存在"""

        Path(root).parent.mkdir(parents=True, exist_ok=True)
        return root

    @classmethod
    def read(cls, path: str, encoding: str = "utf-8") -> str:
        """读取文件"""

        with Path.open(Path(path), encoding=encoding) as f:
            return f.read()

    @classmethod
    def read_json(cls, path: str, encoding: str = "utf-8") -> Dict:
        """读取json文件"""

        return json.loads(cls.read(path, encoding=encoding))

    @classmethod
    def write(cls, path: str, content: str, encoding: str = "utf-8"):
        """写入文件"""

        with Path.open(Path(path), "w", encoding=encoding) as f:
            f.write(content)

    @classmethod
    def write_json(cls, path: str, content: Any, encoding: str = "utf-8"):
        """写入json文件"""

        cls.write(path, json.dumps(content), encoding=encoding)

    @classmethod
    def append(cls, path: str, content: str, encoding: str = "utf-8"):
        """追加写入文件"""

        with Path.open(Path(path), "a", encoding=encoding) as f:
            f.write(content)
