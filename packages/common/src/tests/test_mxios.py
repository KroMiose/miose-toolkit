import asyncio
from typing import TYPE_CHECKING

try:
    import ujson as json  # type: ignore
except ImportError:
    import json

if TYPE_CHECKING:
    from ..miose_toolkit_common import AioResponse, Mxios, Response
else:
    from src.miose_toolkit_common import AioResponse, Mxios, Response


def test_mxios():
    mxios = Mxios(base_url="https://httpbin.org")

    resp: Response = mxios.fetch("get", "/get")
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://httpbin.org/get"

    resp = mxios.get("/get", params={"key": "value"})
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://httpbin.org/get?key=value"
    assert resp.json()["args"] == {"key": "value"}

    resp = mxios.post("/post", data={"key": "value"})
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://httpbin.org/post"
    assert json.loads(resp.json()["data"]) == {"key": "value"}

    resp = mxios.put("/put", data={"key": "value"})
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://httpbin.org/put"
    assert json.loads(resp.json()["data"]) == {"key": "value"}

    resp = mxios.delete("/delete", params={"key": "value"})
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://httpbin.org/delete?key=value"

    async def async_test():
        mxios = Mxios("https://httpbin.org")

        resp: AioResponse = await mxios.async_fetch("get", "/get")
        assert resp.status_code == 200
        assert resp.json()["url"] == "https://httpbin.org/get"

        resp = await mxios.async_get("/get", params={"key": "value"})
        assert resp.status_code == 200
        assert resp.json()["url"] == "https://httpbin.org/get?key=value"
        assert resp.json()["args"] == {"key": "value"}

        resp = await mxios.async_post("/post", data={"key": "value"})
        assert resp.status_code == 200
        assert resp.json()["url"] == "https://httpbin.org/post"
        assert json.loads(resp.json()["data"]) == {"key": "value"}

        resp = await mxios.async_put("/put", data={"key": "value"})
        assert resp.status_code == 200
        assert resp.json()["url"] == "https://httpbin.org/put"
        assert json.loads(resp.json()["data"]) == {"key": "value"}

        resp = await mxios.async_delete("/delete", params={"key": "value"})
        assert resp.status_code == 200
        assert resp.json()["url"] == "https://httpbin.org/delete?key=value"

    asyncio.run(async_test())
