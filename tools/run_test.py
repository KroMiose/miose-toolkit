import os
import sys
from pathlib import Path

from .utils import test_package


def main():
    # 设置 poetry 创建项目内虚拟环境
    os.system("poetry config virtualenvs.in-project true")

    # 初始化主环境
    if (Path() / "poetry.lock").exists():
        os.system("poetry lock --no-update")
    os.system("poetry install")

    # 如果指定了目标包，则只测试目标包
    target_package = sys.argv[1] if len(sys.argv) > 1 else None
    if target_package:
        print(f"Testing package: {target_package}")
        test_package(target_package)
        exit(0)

    # 遍历所有的包
    packages = os.listdir("packages")
    for idx, package in enumerate(packages):
        # 检查是否是目录
        if (Path("packages") / package).is_dir():
            print(f"Testing package {idx + 1}/{len(packages)}: {package}")
            test_package(package)
