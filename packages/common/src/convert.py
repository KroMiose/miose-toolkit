from typing import Any, Optional


class MConvert:
    """转换类"""

    @classmethod
    def safe_int(cls, s: Any, substitute: Optional[int] = None) -> Optional[int]:
        """不会报错的int转换

        :param s: 要转换的任意类型
        """
        try:
            return int(s)
        except Exception:
            return substitute

    @classmethod
    def safe_float(cls, s: Any, substitute: Optional[float] = None) -> Optional[float]:
        """不会报错的float转换

        :param s: 要转换的任意类型
        """
        try:
            return float(s)
        except Exception:
            return substitute
