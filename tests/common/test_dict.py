from miose_toolkit_common import merge_dicts


def test_dict():
    assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert merge_dicts({"a": 1}, {"a": 2}) == {"a": 2}
    assert merge_dicts({"a": 1}, {"a": 2}, {"a": 3}) == {"a": 3}
    assert merge_dicts({"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}) == {"a": 4}
    assert merge_dicts({"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}, {"a": 5}) == {
        "a": 5,
    }

    assert merge_dicts({"a": 1, "b": 2}, {"a": 2}) == {"a": 2, "b": 2}
    assert merge_dicts({"a": 1, "b": 2}, {"a": 2}, {"a": 3}) == {"a": 3, "b": 2}

    assert merge_dicts({"a": 1, "b": 2}, {"a": 2}, {"a": 3}, {"a": 4}) == {
        "a": 4,
        "b": 2,
    }
