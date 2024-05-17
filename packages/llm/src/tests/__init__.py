import os
import re
from importlib import import_module
from pathlib import Path


def main():
    # 获取当前目录
    current_path = Path(__file__).parent
    # 获取当前目录下的所有文件
    files = os.listdir(current_path)

    # 过滤出所有测试文件
    test_files = []
    for file in files:
        if re.match(r"^test_.*\.py$", file):
            test_files.append(file)

    # 执行所有测试文件
    for idx, file in enumerate(test_files):
        file_path = current_path / file
        print(f"Running {idx + 1}/{len(test_files)}: {file_path}")
        # 导入测试模块
        mod = import_module(f".{file[:-3]}", "src.tests")
        # 遍历测试模块中的所有 test_* 方法
        for attr in dir(mod):
            if attr.startswith("test_"):
                # 执行测试方法
                getattr(mod, attr)()


if __name__ == "__main__":
    main()
