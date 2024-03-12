from typing import Dict


def merge_dicts(*args: Dict) -> Dict:
    """合并多个字典的键值对 后面的字典会覆盖前面"""

    res = {}
    for d in args:
        for k, v in d.items():
            if d.get(k):
                res[k] = v
    return res
