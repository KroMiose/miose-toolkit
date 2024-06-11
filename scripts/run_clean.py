import os
import sys
from pathlib import Path

from .utils import clean_package_env


def main():
    # 如果指定了目标包，则只清除目标包
    target_package = sys.argv[1] if len(sys.argv) > 1 else None
    if target_package:
        print(f"Publishing package: {target_package}")
        clean_package_env(target_package)
        exit(0)

    # 遍历所有的包
    packages = os.listdir("packages")
    for idx, package in enumerate(packages):
        # 检查是否是目录
        if (Path("packages") / package).is_dir():
            print(f"Publishing package {idx + 1}/{len(packages)}: {package}")
            clean_package_env(package)
