import os
import re
import time
from pathlib import Path
from typing import Tuple

import requests
import toml

# PROXY = "http://127.0.0.1:7890"
PROXY = None


class enter_package:
    """进入包目录"""

    def __init__(self, package: str):
        self.package = package

    def __enter__(self):
        # 进入包目录
        os.chdir(Path("packages") / self.package)
        time.sleep(0.1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 返回上一级目录
        os.chdir("../..")
        time.sleep(0.1)


def get_current_pkg() -> Tuple[str, str]:
    """获取当前包的名称和版本号"""
    pyproject_text = Path("pyproject.toml").read_text(encoding="utf-8")
    pkg_name, pkg_version = (
        re.findall(r'name ?= ?"(.*)"', pyproject_text)[0],
        re.findall(r'version ?= ?"(.*)"', pyproject_text)[0],
    )

    if pkg_name and pkg_version:
        return pkg_name, pkg_version
    raise Exception("No valid pyproject.toml found.")


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
        print(f"Installing package {package}...")

        # 获取所有 extras
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            pyproject_content = toml.load(pyproject_path)
            extras = (
                pyproject_content.get("tool", {}).get("poetry", {}).get("extras", {})
            )
            all_extras = list(extras.keys())
        else:
            all_extras = []

        if Path("poetry.lock").exists():
            # 更新 poetry.lock
            os.system("poetry lock --no-update")

        # 安装依赖
        if all_extras:
            extras_str = "all" if "all" in all_extras else ",".join(all_extras)
            os.system(f"poetry install -E {extras_str}")
        else:
            os.system("poetry install")

    print(f"Package {pkg_name} install success!\n")


def clean_package_env(package: str):
    """清理包环境"""
    with enter_package(package):
        pkg_name, pkg_version = get_current_pkg()
        # 删除构建文件
        for file in Path("dist").glob("*"):
            file.unlink()
        # 删除缓存文件
        for file in Path("build").glob("*"):
            file.unlink()
        # 删除 .venv 目录
        if Path(".venv").exists():
            for file in Path(".venv").glob("*"):
                file.unlink()
            Path(".venv").rmdir()

    print(f"Package {pkg_name} clean success!\n")


def test_package(package: str):
    """测试包"""
    # install_package(package)

    with enter_package(package):
        pkg_name, pkg_version = get_current_pkg()
        # 执行测试
        pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
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


def build_package(package: str):
    """构建包"""
    # install_package(package)

    with enter_package(package):
        pkg_name, pkg_version = get_current_pkg()
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


def publish_package(package: str):
    """发布包"""
    with enter_package(package):
        pkg_name, pkg_version = get_current_pkg()
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
