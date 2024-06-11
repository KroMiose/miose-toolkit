from miose_toolkit_common import (
    drop_url_anchor,
    get_url_domain,
    get_url_params,
    get_url_path,
    is_relative_url,
)


def test_url():
    assert get_url_params("http://example.com") == {}
    assert get_url_params("http://example.com?a=1") == {"a": "1"}
    assert get_url_params("http://example.com?a=1&b=2") == {"a": "1", "b": "2"}
    assert get_url_params("http://example.com?a=1&b=2&c=3") == {
        "a": "1",
        "b": "2",
        "c": "3",
    }
    assert get_url_params("http://example.com?a=1&b=2&c=3&d=4") == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
    }
    assert get_url_params("http://example.com?a=1&b=2&c=3&d=4&e=5") == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "e": "5",
    }
    assert get_url_params("http://example.com?a=1&b=2&c=3&d=4&e=5&f=6") == {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "e": "5",
        "f": "6",
    }

    assert get_url_params(
        "http://example.com?quote=%E4%B8%AD%E6%96%87",
        False,
    ) == {
        "quote": "%E4%B8%AD%E6%96%87",
    }
    assert get_url_params("http://example.com?quote=%E4%B8%AD%E6%96%87") == {
        "quote": "中文",
    }

    assert get_url_domain("http://example.com") == "example.com"
    assert get_url_domain("http://example.com/") == "example.com"

    assert get_url_path("http://example.com") == "/"
    assert get_url_path("http://example.com/") == "/"
    assert get_url_path("http://example.com/path") == "/path"
    assert get_url_path("http://example.com/path/") == "/path/"
    assert get_url_path("http://example.com/path/to") == "/path/to"
    assert get_url_path("http://example.com/path/to/") == "/path/to/"

    assert drop_url_anchor("http://example.com") == "http://example.com"
    assert drop_url_anchor("http://example.com/") == "http://example.com/"
    assert drop_url_anchor("http://example.com/path") == "http://example.com/path"
    assert drop_url_anchor("http://example.com/path/") == "http://example.com/path/"

    assert drop_url_anchor("http://example.com#") == "http://example.com"
    assert drop_url_anchor("http://example.com/#") == "http://example.com/"
    assert drop_url_anchor("http://example.com/path#") == "http://example.com/path"
    assert drop_url_anchor("http://example.com/path/#") == "http://example.com/path/"

    assert drop_url_anchor("http://example.com#anchor") == "http://example.com"
    assert drop_url_anchor("http://example.com/#anchor") == "http://example.com/"

    assert is_relative_url("/") is True
    assert is_relative_url("#") is True
    assert is_relative_url("/path") is True
    assert is_relative_url("/path/") is True
    assert is_relative_url("/path/to") is True
    assert is_relative_url("/path/to/") is True

    assert is_relative_url("http://example.com") is False
    assert is_relative_url("http://example.com/") is False
    assert is_relative_url("http://example.com/path") is False
