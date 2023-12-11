from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..src import MUrl
else:
    from src import MUrl


def test_url():
    assert MUrl.get_url_params("http://example.com") == {}
    assert MUrl.get_url_params("http://example.com?a=1") == {"a": "1"}
    assert MUrl.get_url_params("http://example.com?a=1&b=2") == {"a": "1", "b": "2"}
    assert MUrl.get_url_params("http://example.com?a=1&b=2&c=3") == {
        "a": "1",
        "b": "2",
        "c": "3",
    }
    assert MUrl.get_url_params("http://example.com?a=1&b=2&c=3&d=4") == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
    }
    assert MUrl.get_url_params("http://example.com?a=1&b=2&c=3&d=4&e=5") == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "e": "5",
    }
    assert MUrl.get_url_params("http://example.com?a=1&b=2&c=3&d=4&e=5&f=6") == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "e": "5",
        "f": "6",
    }

    assert MUrl.get_url_params(
        "http://example.com?quote=%E4%B8%AD%E6%96%87", False
    ) == {
        "quote": "%E4%B8%AD%E6%96%87",
    }
    assert MUrl.get_url_params("http://example.com?quote=%E4%B8%AD%E6%96%87") == {
        "quote": "中文",
    }

    assert MUrl.get_url_domain("http://example.com") == "example.com"
    assert MUrl.get_url_domain("http://example.com/") == "example.com"

    assert MUrl.get_url_path("http://example.com") == "/"
    assert MUrl.get_url_path("http://example.com/") == "/"
    assert MUrl.get_url_path("http://example.com/path") == "/path"
    assert MUrl.get_url_path("http://example.com/path/") == "/path/"
    assert MUrl.get_url_path("http://example.com/path/to") == "/path/to"
    assert MUrl.get_url_path("http://example.com/path/to/") == "/path/to/"

    assert MUrl.drop_url_anchor("http://example.com") == "http://example.com"
    assert MUrl.drop_url_anchor("http://example.com/") == "http://example.com/"
    assert MUrl.drop_url_anchor("http://example.com/path") == "http://example.com/path"
    assert (
        MUrl.drop_url_anchor("http://example.com/path/") == "http://example.com/path/"
    )

    assert MUrl.drop_url_anchor("http://example.com#") == "http://example.com"
    assert MUrl.drop_url_anchor("http://example.com/#") == "http://example.com/"
    assert MUrl.drop_url_anchor("http://example.com/path#") == "http://example.com/path"
    assert (
        MUrl.drop_url_anchor("http://example.com/path/#") == "http://example.com/path/"
    )

    assert MUrl.drop_url_anchor("http://example.com#anchor") == "http://example.com"
    assert MUrl.drop_url_anchor("http://example.com/#anchor") == "http://example.com/"

    assert MUrl.is_relative_url("/") is True
    assert MUrl.is_relative_url("#") is True
    assert MUrl.is_relative_url("/path") is True
    assert MUrl.is_relative_url("/path/") is True
    assert MUrl.is_relative_url("/path/to") is True
    assert MUrl.is_relative_url("/path/to/") is True

    assert MUrl.is_relative_url("http://example.com") is False
    assert MUrl.is_relative_url("http://example.com/") is False
    assert MUrl.is_relative_url("http://example.com/path") is False
