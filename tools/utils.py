import os
from pathlib import Path
from typing import Tuple

import requests

# PROXY = "http://127.0.0.1:7890"
PROXY = None


class enter_package:
    """进入包目录"""

    def __init__(self, package: str):
        self.package = package

    def __enter__(self):
        # 进入包目录
        os.chdir(Path("packages") / self.package)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 返回上一级目录
        os.chdir("../..")


def get_current_pkg() -> Tuple[str, str]:
    """获取当前包的名称和版本号"""
    try:
        return (
            Path("pyproject.toml").read_text().split('name = "')[1].split('"')[0],
            Path("pyproject.toml").read_text().split('version = "')[1].split('"')[0],
        )
    except Exception:
        return "", ""


def fetch_pkg_latest_version(pkg_name: str, proxy=PROXY) -> str:
    """在线获取包最新版本号"""
    try:
        res = requests.get(
            f"https://pypi.org/pypi/{pkg_name}/json",
            proxies={"http": proxy, "https": proxy} if proxy else None,
        ).json()
    except Exception:
        return ""

    try:
        if res["info"]["version"]:
            return res["info"]["version"]
    except Exception:
        pass
    try:
        if res["message"] == "Not Found":
            return "-"
    except Exception:
        pass
    return ""


def install_package(package: str):
    """安装包与依赖"""
    with enter_package(package):
        pkg_name, pkg_version = get_current_pkg()
        if pkg_name:
            print(f"Installing package {package}...")
            if Path("poetry.lock").exists():
                # 更新 poetry.lock
                os.system("poetry lock --no-update")
            # 安装依赖
            os.system("poetry install")
        else:
            print("No pyproject.toml found. Skipping...")


def test_package(package: str):
    """测试包"""
    install_package(package)

    with enter_package(package):
        pkg_name, pkg_version = get_current_pkg()
        if pkg_name:
            # 执行测试
            pyproject = Path("pyproject.toml").read_text()
            if "test" in pyproject:
                print("Running tests...")
                try:
                    assert os.system("poetry run test") == 0
                except AssertionError:
                    print(f"Package {pkg_name} test failed.")
                    exit(1)
            else:
                print("No tests found. Skipping...")

            print(f"Package {pkg_name} test passed.\n")
        else:
            print("No pyproject.toml found. Skipping...")


def build_package(package: str):
    """构建包"""
    install_package(package)

    with enter_package(package):
        pkg_name, pkg_version = get_current_pkg()
        if pkg_name:
            # 删除旧的构建文件
            for file in Path("dist").glob("*"):
                file.unlink()
            # 执行构建
            try:
                assert os.system("poetry build") == 0
            except AssertionError:
                print(f"Package {pkg_name} build failed.")
                exit(1)

            print(f"Package {pkg_name} build success!\n")
        else:
            print("No pyproject.toml found. Skipping...")


def publish_package(package: str):
    """发布包"""
    with enter_package(package):
        pkg_name, pkg_version = get_current_pkg()
        if pkg_name:
            # 检查是否已经发布
            latest_version = fetch_pkg_latest_version(pkg_name)
            if latest_version == pkg_version:
                print(f"Package {pkg_name} is already published.")
                return
            # 执行发布
            try:
                assert os.system("poetry publish") == 0
            except AssertionError:
                print(f"Package {pkg_name} publish failed.")
                exit(1)

            print(f"Package {pkg_name} publish success!\n")
        else:
            print("No pyproject.toml found. Skipping...")
