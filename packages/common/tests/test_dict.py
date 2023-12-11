from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..src import MDict
else:
    from src import MDict


def test_dict():
    assert MDict.merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert MDict.merge_dicts({"a": 1}, {"a": 2}) == {"a": 2}
    assert MDict.merge_dicts({"a": 1}, {"a": 2}, {"a": 3}) == {"a": 3}
    assert MDict.merge_dicts({"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}) == {"a": 4}
    assert MDict.merge_dicts({"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}, {"a": 5}) == {
        "a": 5,
    }

    assert MDict.merge_dicts({"a": 1, "b": 2}, {"a": 2}) == {"a": 2, "b": 2}
    assert MDict.merge_dicts({"a": 1, "b": 2}, {"a": 2}, {"a": 3}) == {"a": 3, "b": 2}

    assert MDict.merge_dicts({"a": 1, "b": 2}, {"a": 2}, {"a": 3}, {"a": 4}) == {
        "a": 4,
        "b": 2,
    }
