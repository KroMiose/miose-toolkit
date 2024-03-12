from typing import List

try:
    import ujson as json
except ImportError:
    import json


def quick_value(ls: List, substitute: str = "") -> str:
    """快速列表取值"""
    if isinstance(ls, str):
        return ls.strip() if (ls and ls.strip()) else substitute
    if len(ls) == 0:
        return substitute
    return ls[0].strip() if (ls[0] and ls[0].strip()) else substitute

def drop_empty_from_list(lst: List) -> List[str]:
    """去除列表中的空字符串元素"""

    return [i for i in lst if i and i.strip()]

def split_and_drop_empty(s: str, sep: str) -> List[str]:
    """切割字符串并去除空字符串元素"""
    return drop_empty_from_list(s.split(sep))

def json_list_stringify_limit(lst: List, limit=1024) -> str:
    """列表转json列表长度自动限制(丢弃超出限制的元素)"""
    while True:
        if len(lst) < 1:
            return "[]"
        res = json.dumps(lst, ensure_ascii=False)
        if len(res) <= limit:
            return res
        lst = lst[:-1]

def advance_split(s: str, sep: str, filter_empty=True) -> List[str]:
    """高级切割字符串 (支持单双引号配对防截断和引号转义)"""
    res = []
    temp = ""
    in_single_quote = False
    in_double_quote = False
    escape = False
    for i in s:
        if escape:
            temp += i
            escape = False
            continue
        if i == "\\":
            escape = True
            continue
        if i == "'":
            in_single_quote = not in_single_quote
        if i == '"':
            in_double_quote = not in_double_quote
        if i == sep and not in_single_quote and not in_double_quote:
            res.append(temp)
            temp = ""
        else:
            temp += i
    res.append(temp)

    # 过滤空字符串
    if filter_empty:
        res = [i for i in res if i.strip()]

    # 去除引号
    res = [i[1:-1] if i.startswith('"') and i.endswith('"') else i for i in res]
    res = [i[1:-1] if i.startswith("'") and i.endswith("'") else i for i in res]

    return res  # noqa: RET504
