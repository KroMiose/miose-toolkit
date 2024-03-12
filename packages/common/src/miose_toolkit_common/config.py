import sys
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

import yaml
from pydantic import BaseModel

from .common import Version, get_pkg_version

__pydantic_version__: Version = Version(get_pkg_version("pydantic"))
_config_root: Path = Path("./configs")

class Env(Enum):
    """预设环境变量"""

    Local = "local"
    Dev = "dev"
    Test = "test"
    Prod = "prod"
    Custom = "custom"
    Default = "dev"  # noqa: PIE796


APP_ENV: str = Env.Default.value


class Config(BaseModel):
    """配置基类"""

    @classmethod
    def set_configs_root(cls, root: Union[str, Path]):
        """设置配置文件根目录"""
        global _config_root
        _config_root = Path(root)

    @classmethod
    def load_config(cls, create_if_not_exists: bool = True):
        """加载配置

        :param create_if_not_exists: 如果配置文件不存在，是否创建

        :raises Exception: 配置文件格式错误
        """

        global APP_ENV, _config_root
        config_path = _config_root / f"config.{APP_ENV}.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with config_path.open("r") as file:
                if __pydantic_version__ < Version("2.0.0"):  # 兼容旧版本的 pydantic
                    obj = cls.parse_obj(yaml.safe_load(file))
                else:
                    obj = cls.model_validate(yaml.safe_load(file))
        except Exception:
            if create_if_not_exists:
                cls.dump_config_template()
                return cls.load_config(False)
            raise
        try:
            if __pydantic_version__ < Version("2.0.0"):
                return cls.parse_obj(obj)
            return cls.model_validate(obj)
        except Exception as e:
            raise Exception(f"配置文件格式错误: {e}") from e

    @classmethod
    def dump_modal(cls):
        """导出配置模板

        :return: 配置模板
        """
        return cls().__dict__

    @classmethod
    def dump_config_template(cls, envs: Optional[List[str]] = None):
        """导出配置模板"""

        global _config_root
        if envs is None:
            envs = [APP_ENV]
        for env in envs:
            config_path = _config_root / f"config.{env}.yaml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                yaml.dump(cls.dump_modal(), allow_unicode=True, sort_keys=False),
            )
        return cls.dump_modal()

    def dump_config(self, envs: Optional[List[str]] = None):
        """导出配置"""

        global _config_root
        if envs is None:
            envs = [APP_ENV]
        for env in envs:
            config_path = _config_root / f"config.{env}.yaml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            if config_path.exists():
                # 如果配置文件存在，则只补充缺失的配置项
                origin_config = yaml.safe_load(config_path.read_text())
                for key, value in self.__dict__.items():
                    if key not in origin_config:
                        origin_config[key] = value
                config_path.write_text(
                    yaml.dump(origin_config, allow_unicode=True, sort_keys=False),
                )
            else:
                config_path.write_text(
                    yaml.dump(self.model_dump(), allow_unicode=True, sort_keys=False),
                )

    def reload_config(self):
        """重新加载配置"""
        obj = self.load_config()
        self.__dict__.update(obj.__dict__)

    def gen_config_schema(self):
        """生成配置结构

        :return: 配置结构
        """
        if __pydantic_version__ < Version("2.0.0"):
            return self.schema()["properties"]
        return self.__class__.model_json_schema()["properties"]


for arg in sys.argv[1:]:
    if arg.startswith("env="):
        target_env = arg.split("=")[-1]
        for env in Env:
            if env.value.lower() == target_env.lower():
                APP_ENV = env.value
                break
        else:
            raise Exception(f'环境变量 "{target_env}" 不存在')
        break
else:
    APP_ENV = Env.Default.value
