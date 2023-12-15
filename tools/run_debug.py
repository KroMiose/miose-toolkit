import os
import sys
from pathlib import Path

from .utils import debug_package


def main():
    # 设置 poetry 创建项目内虚拟环境
    os.system("poetry config virtualenvs.in-project true")

    # 初始化主环境
    if (Path() / "poetry.lock").exists():
        os.system("poetry lock --no-update")
    os.system("poetry install")

    # 调试目标包
    target_package = sys.argv[1] if len(sys.argv) > 1 else None
    if target_package:
        print(f"Testing package: {target_package}")
        debug_package(target_package)
        exit(0)
    else:
        raise Exception("No target package.")


if __name__ == "__main__":
    main()
