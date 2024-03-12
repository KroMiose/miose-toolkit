from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..miose_toolkit_common import Version
else:
    from src.miose_toolkit_common import Version


def test_common():
    assert Version("1.0.0") < Version("2.0.0")
    assert Version("1.0.0") <= Version("2.0.0")
    assert Version("1.10.0") <= Version("2.0.0")
    assert Version("1.0.0") == Version("1.0.0")
    assert Version("1.0.0") != Version("10.0.0")
    assert Version("2.0.0") > Version("1.0.0")
    assert Version("2.0.0") >= Version("1.0.0")
    assert str(Version("1.0.0")) == "1.0.0"
