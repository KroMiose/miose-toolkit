# Miose Toolkit 工具箱: Logger 子项目

## 介绍

Logger 子项目包含了一个简单易用的日志工具。

## 测试用例库 -> [用例库](./src/tests)

测试用例库中包含了所有模块的测试用例，可以参考其中的代码来使用模块。

## 功能列表

### 0. 引入与初始化设定

```python
from miose_toolkit_logger import logger

# 设置日志等级
logger.set_log_level("DEBUG")

# 设置日志格式
logger.set_log_format(
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "<c>{function}:{line}</c>| "
    "{message}",
)

# 设置日志输出到文件 (with_console=True 表示同时输出到控制台)
logger.set_log_output("test.log", with_console=True)

# 重置日志输出
logger.unset_log_output()
```

### 1. 使用日志

```python
# 输出调试信息
logger.debug("This is a debug message.")

# 输出信息
logger.info("This is an info message.")

# 输出警告
logger.warning("This is a warning message.")

# 输出错误
logger.error("This is an error message.")

# 输出严重错误
logger.critical("This is a critical message.")

# 输出成功信息
logger.success("This is a success message.")
```
