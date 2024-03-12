from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..miose_toolkit_common import (
        advance_split,
        drop_empty_from_list,
        json_list_stringify_limit,
        quick_value,
        split_and_drop_empty,
    )
else:
    from src.miose_toolkit_common import (
        advance_split,
        drop_empty_from_list,
        json_list_stringify_limit,
        quick_value,
        split_and_drop_empty,
    )


def test_list():
    assert quick_value(["1", "2", "3"]) == "1"
    assert quick_value(["", "2", "3"]) == ""
    assert quick_value(["123"]) == "123"
    assert quick_value([""]) == ""
    assert quick_value("1233") == "1233"  # type: ignore

    assert drop_empty_from_list(["1", "2", "3"]) == ["1", "2", "3"]
    assert drop_empty_from_list(["1", "", "3"]) == ["1", "3"]
    assert drop_empty_from_list(["1", "2", ""]) == ["1", "2"]
    assert drop_empty_from_list(["", "2", "3"]) == ["2", "3"]
    assert drop_empty_from_list(["1", "", ""]) == ["1"]
    assert drop_empty_from_list([None, "2", "3"]) == ["2", "3"]
    assert drop_empty_from_list(["1", None, "3"]) == ["1", "3"]
    assert drop_empty_from_list(["1", "2", None]) == ["1", "2"]
    assert drop_empty_from_list(["1", "2", " "]) == ["1", "2"]
    assert drop_empty_from_list([None, None, None]) == []
    assert drop_empty_from_list([]) == []

    assert split_and_drop_empty("1,2,3", ",") == ["1", "2", "3"]
    assert split_and_drop_empty("1,,3", ",") == ["1", "3"]
    assert split_and_drop_empty("1,2,", ",") == ["1", "2"]
    assert split_and_drop_empty(",2,3", ",") == ["2", "3"]
    assert split_and_drop_empty("1,,", ",") == ["1"]
    assert split_and_drop_empty("1, ,", ",") == ["1"]
    assert split_and_drop_empty("1, , ", ",") == ["1"]

    assert json_list_stringify_limit(["1", "2", "3"], 1024) == '["1","2","3"]'
    assert json_list_stringify_limit(["1", "2", "3"], 10) == '["1","2"]'
    assert json_list_stringify_limit(["1", "2", "3"], 4) == "[]"
    assert json_list_stringify_limit(["1", "2", "3"], 3) == "[]"

    assert advance_split("1,2,3", ",") == ["1", "2", "3"]
    assert advance_split("1,,3", ",") == ["1", "3"]
    assert advance_split("1,2,", ",") == ["1", "2"]

    assert advance_split("1,2,3", ",", filter_empty=False) == ["1", "2", "3"]
    assert advance_split("1,,3", ",", filter_empty=False) == ["1", "", "3"]
    assert advance_split("1,2,", ",", filter_empty=False) == ["1", "2", ""]

    assert advance_split("command 'a b c'", " ") == ["command", "a b c"]
    assert advance_split("command  'a b c' test ", " ") == [
        "command",
        "a b c",
        "test",
    ]
    assert advance_split("command  'a b c' test ", " ", filter_empty=False) == [
        "command",
        "",
        "a b c",
        "test",
        "",
    ]
