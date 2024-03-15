import contextlib
import os
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

try:
    import ujson as json
except ImportError:
    import json

if TYPE_CHECKING:
    from ..miose_toolkit_common import APP_ENV, Config, Env
else:
    from src.miose_toolkit_common import APP_ENV, Config, Env


def test_config():
    # 验证环境变量
    assert Env.Default.value == APP_ENV

    # 清除测试用的临时文件(如果存在)
    Path("./temp/test_configs/config.dev.yaml").unlink(True)
    Path("./temp/test_configs/config.test.yaml").unlink(True)
    Path("./temp/test_configs/config.prod.yaml").unlink(True)
    with contextlib.suppress(OSError):
        Path("./temp/test_configs").rmdir()

    # 测试配置模板
    class TestConfigTemplate(Config):
        a: int = 1
        b: str = "b"

    # 测试加载配置
    Config.set_configs_root("./temp/test_configs")
    config = TestConfigTemplate.load_config(True)
    assert config.a == 1
    assert config.b == "b"
    config.a = 2
    config.dump_config()
    config = TestConfigTemplate.load_config()
    assert config.a == 1
    assert config.b == "b"
    config.a = 3
    config.dump_config([Env.Dev.value])

    # 验证导出配置模板
    load_data = yaml.safe_load(Path("./temp/test_configs/config.dev.yaml").read_text())
    assert load_data["a"] == 1
    assert load_data["b"] == "b"

    # 测试重载配置
    load_data["a"] = 4
    load_data["b"] = "c"
    with Path("./temp/test_configs/config.dev.yaml").open("w") as file:
        yaml.safe_dump(load_data, file)
    config.reload_config()
    assert config.a == 4
    assert config.b == "c"

    # 测试生成配置结构
    # print(config.gen_config_schema())
    assert config.gen_config_schema() == {
        "a": {"title": "A", "default": 1,"type": "integer"},
        "b": {"title": "B", "default": "b","type": "string"},
    }

    # 删除测试用的临时文件
    Path("./temp/test_configs/config.dev.yaml").unlink(True)
    Path("./temp/test_configs/config.test.yaml").unlink(True)
    Path("./temp/test_configs/config.prod.yaml").unlink(True)
    Path("./temp/test_configs").rmdir()

    # 测试加载不存在的配置
    try:
        config.reload_config()
        raise AssertionError  # noqa: TRY301
    except Exception:
        assert True
