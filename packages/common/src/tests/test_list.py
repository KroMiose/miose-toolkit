from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..miose_toolkit_common import MList
else:
    from miose_toolkit_common import MList


def test_list():
    assert MList.quick_value(["1", "2", "3"]) == "1"
    assert MList.quick_value(["", "2", "3"]) == ""
    assert MList.quick_value(["123"]) == "123"
    assert MList.quick_value([""]) == ""
    assert MList.quick_value("1233") == "1233"  # type: ignore

    assert MList.drop_empty_from_list(["1", "2", "3"]) == ["1", "2", "3"]
    assert MList.drop_empty_from_list(["1", "", "3"]) == ["1", "3"]
    assert MList.drop_empty_from_list(["1", "2", ""]) == ["1", "2"]
    assert MList.drop_empty_from_list(["", "2", "3"]) == ["2", "3"]
    assert MList.drop_empty_from_list(["1", "", ""]) == ["1"]
    assert MList.drop_empty_from_list([None, "2", "3"]) == ["2", "3"]
    assert MList.drop_empty_from_list(["1", None, "3"]) == ["1", "3"]
    assert MList.drop_empty_from_list(["1", "2", None]) == ["1", "2"]
    assert MList.drop_empty_from_list(["1", "2", " "]) == ["1", "2"]
    assert MList.drop_empty_from_list([None, None, None]) == []
    assert MList.drop_empty_from_list([]) == []

    assert MList.split_and_drop_empty("1,2,3", ",") == ["1", "2", "3"]
    assert MList.split_and_drop_empty("1,,3", ",") == ["1", "3"]
    assert MList.split_and_drop_empty("1,2,", ",") == ["1", "2"]
    assert MList.split_and_drop_empty(",2,3", ",") == ["2", "3"]
    assert MList.split_and_drop_empty("1,,", ",") == ["1"]
    assert MList.split_and_drop_empty("1, ,", ",") == ["1"]
    assert MList.split_and_drop_empty("1, , ", ",") == ["1"]

    assert MList.json_list_stringify_limit(["1", "2", "3"], 1024) == '["1","2","3"]'
    assert MList.json_list_stringify_limit(["1", "2", "3"], 10) == '["1","2"]'
    assert MList.json_list_stringify_limit(["1", "2", "3"], 4) == "[]"
    assert MList.json_list_stringify_limit(["1", "2", "3"], 3) == "[]"

    assert MList.advance_split("1,2,3", ",") == ["1", "2", "3"]
    assert MList.advance_split("1,,3", ",") == ["1", "3"]
    assert MList.advance_split("1,2,", ",") == ["1", "2"]

    assert MList.advance_split("1,2,3", ",", filter_empty=False) == ["1", "2", "3"]
    assert MList.advance_split("1,,3", ",", filter_empty=False) == ["1", "", "3"]
    assert MList.advance_split("1,2,", ",", filter_empty=False) == ["1", "2", ""]

    assert MList.advance_split("command 'a b c'", " ") == ["command", "a b c"]
    assert MList.advance_split("command  'a b c' test ", " ") == [
        "command",
        "a b c",
        "test",
    ]
    assert MList.advance_split("command  'a b c' test ", " ", filter_empty=False) == [
        "command",
        "",
        "a b c",
        "test",
        "",
    ]
