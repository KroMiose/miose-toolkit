import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal, Union

from loguru import logger as _logger
from loguru._logger import Logger as __Logger

if TYPE_CHECKING:
    from loguru import Record as LoguruRecord

_LOGGER_FORMAT: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    # "<c>{function}:{line}</c>| "
    "{message}"
)

_LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
_LOG_OUTPUT = sys.stdout


def _default_filter(record: "LoguruRecord"):
    def abstract_filter(error_no: int) -> bool:
        config_no = (
            _logger.level(_LOG_LEVEL).no if isinstance(_LOG_LEVEL, str) else _LOG_LEVEL
        )
        return error_no >= config_no or record["message"] == "success"

    return abstract_filter(record["level"].no)


_logger.add(
    _LOG_OUTPUT,
    level=0,
    diagnose=False,
    filter=_default_filter,
    format=_LOGGER_FORMAT,
)


def _set_log_level(level: str):
    """设置日志级别
    Args:
        level (str): 日志级别 DEBUG, INFO, WARNING, ERROR, CRITICAL
    """
    global _LOG_LEVEL
    level = level.upper()
    if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError("Invalid log level.")
    _LOG_LEVEL = level  # type: ignore
    _logger.remove()
    _logger.add(
        _LOG_OUTPUT,
        level=0,
        diagnose=False,
        filter=_default_filter,
        format=_LOGGER_FORMAT,
    )


def _set_log_format(_format: str):
    """设置日志格式
    Args:
        format (str): 日志格式 示例: "<g>{time:MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u>{name}</u></c> | {message}" 可用变量: time, level, name, function, line, message
    """
    global _LOGGER_FORMAT
    _LOGGER_FORMAT = _format
    _logger.remove()
    _logger.add(
        _LOG_OUTPUT,
        level=0,
        diagnose=False,
        filter=_default_filter,
        format=_LOGGER_FORMAT,
    )


def _set_log_output(output: Union[str, Path], with_console: bool = True):
    """设置日志输出
    Args:
        output (str): 日志输出 示例: "logs/{time:YYYY-MM-DD}.log" 可用变量: time
    """
    global _LOG_OUTPUT
    _LOG_OUTPUT = output if isinstance(output, str) else str(output)
    Path(_LOG_OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    _logger.remove()
    _logger.add(
        _LOG_OUTPUT,
        level=0,
        diagnose=False,
        filter=_default_filter,
        format=_LOGGER_FORMAT,
    )
    if with_console:
        _logger.add(
            sys.stdout,
            level=0,
            diagnose=False,
            filter=_default_filter,
            format=_LOGGER_FORMAT,
        )


def _unset_log_output():
    """取消日志输出"""
    global _LOG_OUTPUT
    _LOG_OUTPUT = sys.stdout
    _logger.remove()
    _logger.add(
        _LOG_OUTPUT,
        level=0,
        diagnose=False,
        filter=_default_filter,
        format=_LOGGER_FORMAT,
    )


def _on_log():
    """日志内容处理回调装饰器
    Args:
        callback (Callable[[str], Any]): 处理日志文本的回调函数
    """

    def decorator(func: Callable[[str], Any]):
        def wrapper(msg: str):
            func(msg)

        return wrapper

    return decorator


class _Logger(__Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.on_log = _on_log

    def set_log_level(self, level: str):
        """设置日志级别
        Args:
            level (str): 日志级别 DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
        _set_log_level(level)

    def set_log_format(self, _format: str):
        """设置日志格式
        Args:
            format (str): 日志格式 示例: "<g>{time:MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u>{name}</u></c> | {message}" 可用变量: time, level, name, function, line, message
        """
        _set_log_format(_format)

    def set_log_output(self, output: Union[str, Path], with_console: bool = True):
        """设置日志输出
        Args:
            output (str): 日志输出 示例: "logs/{time:YYYY-MM-DD}.log" 可用变量: time
        """
        _set_log_output(output, with_console)

    def unset_log_output(self):
        """取消日志输出"""
        _unset_log_output()


logger: _Logger = _logger  # type: ignore
logger.set_log_level = _set_log_level
logger.set_log_format = _set_log_format
logger.set_log_output = _set_log_output
logger.unset_log_output = _unset_log_output
# logger.on_log = _on_log
