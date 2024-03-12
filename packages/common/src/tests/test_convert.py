from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..miose_toolkit_common import safe_float, safe_int
else:
    from src.miose_toolkit_common import safe_float, safe_int


def test_convert():
    assert safe_int("1") == 1
    assert safe_int("1.1") is None
    assert safe_int("1.1", 0) == 0
    assert safe_float("1.1") == 1.1
    assert safe_float("1") == 1.0
    assert safe_float("1.1.1") is None
    assert safe_float("1.1.1", 0.0) == 0.0
    assert safe_float("1.1.1", 0) == 0
    assert safe_float("1.1.1", None) is None
    return
