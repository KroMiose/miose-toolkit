from typing import List

try:
    import ujson as json
except ImportError:
    import json


class MList(list):
    """列表类"""

    @classmethod
    def quick_value(cls, ls: List, substitute: str = "") -> str:
        """快速列表取值"""
        if len(ls) == 0:
            return substitute
        return ls[0].strip() if (ls[0] and ls[0].strip()) else substitute

    @classmethod
    def drop_empty_from_list(cls, lst: List) -> List[str]:
        """去除列表中的空字符串元素"""

        return [i for i in lst if i.strip()]

    @classmethod
    def split_and_drop_empty(cls, s: str, sep: str) -> List[str]:
        """切割字符串并去除空字符串元素"""
        return [i.strip() for i in s.split(sep) if i.strip()]

    @classmethod
    def json_list_stringify_limit(cls, lst: List, limit=1024) -> str:
        """列表转json列表长度自动限制(丢弃超出限制的元素)"""
        while True:
            if len(lst) < 1:
                return "[]"
            res = json.dumps(lst, ensure_ascii=False)
            if len(res) <= limit:
                return res
            lst = lst[:-1]
