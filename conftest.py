import os
import shutil
import sys
from pathlib import Path

import pytest

os.environ["IN_TEST_MODE"] = "true"

# enable_stop_on_exceptions if the debugger is running during a test
if "debugpy" in sys.modules:

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call):
        raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo):
        raise excinfo.value


@pytest.fixture(scope="session", autouse=True)
def clean_temp_folder():
    """清理 temp 文件夹。

    这个 fixture 使用以下参数:

    * scope="session": 表示这个 fixture 的作用范围是整个测试会话，即在所有测试开始前执行一次，在所有测试结束后再执行一次。
    * autouse=True:  表示自动使用这个 fixture，无需在测试函数中显式声明。
    """

    temp_folder = Path("temp")
    if temp_folder.exists():
        shutil.rmtree(temp_folder)
    temp_folder.mkdir(exist_ok=True)

    yield

    # shutil.rmtree(temp_folder)
