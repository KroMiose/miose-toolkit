import os
from pathlib import Path


class enter_package:
    def __init__(self, package: str):
        self.package = package

    def __enter__(self):
        # 进入包目录
        os.chdir(Path("packages") / self.package)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 返回上一级目录
        os.chdir("../..")


def install_package(package: str):
    with enter_package(package):
        # 检查是否存在 pyproject.toml
        if Path("pyproject.toml").exists():
            print("Installing dependencies...")
            if Path("poetry.lock").exists():
                # 更新 poetry.lock
                os.system("poetry lock --no-update")
            # 安装依赖
            os.system("poetry install")
        else:
            print("No pyproject.toml found. Skipping...")


def test_package(package: str):
    install_package(package)

    with enter_package(package):
        # 检查是否存在 pyproject.toml
        if Path("pyproject.toml").exists():
            # 执行测试
            pyproject = Path("pyproject.toml").read_text()
            if "test" in pyproject:
                print("Running tests...")
                try:
                    assert os.system("poetry run test") == 0
                except AssertionError:
                    print(f"Package {package} test failed.")
                    exit(1)
            else:
                print("No tests found. Skipping...")

            print(f"Package {package} test passed.")
        else:
            print("No pyproject.toml found. Skipping...")


def build_package(package: str):
    test_package(package)

    with enter_package(package):
        # 检查是否存在 pyproject.toml
        if Path("pyproject.toml").exists():
            # 删除旧的构建文件
            for file in Path("dist").glob("*"):
                file.unlink()
            # 执行构建
            try:
                assert os.system("poetry build") == 0
            except AssertionError:
                print(f"Package {package} build failed.")
                exit(1)

            print(f"Package {package} build success!")
        else:
            print("No pyproject.toml found. Skipping...")


def publish_package(package: str):
    with enter_package(package):
        # 检查是否存在 pyproject.toml
        if Path("pyproject.toml").exists():
            # 执行发布
            try:
                assert os.system("poetry publish") == 0
            except AssertionError:
                print(f"Package {package} publish failed.")
                exit(1)

            print(f"Package {package} publish success!")
        else:
            print("No pyproject.toml found. Skipping...")
