from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..miose_toolkit_common import MConvert
else:
    from miose_toolkit_common import MConvert


def test_convert():
    assert MConvert.safe_int("1") == 1
    assert MConvert.safe_int("1.1") is None
    assert MConvert.safe_int("1.1", 0) == 0
    assert MConvert.safe_float("1.1") == 1.1
    assert MConvert.safe_float("1") == 1.0
    assert MConvert.safe_float("1.1.1") is None
    assert MConvert.safe_float("1.1.1", 0.0) == 0.0
    assert MConvert.safe_float("1.1.1", 0) == 0
    assert MConvert.safe_float("1.1.1", None) is None
    return
