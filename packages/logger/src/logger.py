import sys
from typing import TYPE_CHECKING, Any, Callable

from loguru import logger as _logger
from loguru._logger import Logger as __Logger

if TYPE_CHECKING:
    from loguru import Record as LoguruRecord

_LOGGER_FORMAT = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    # "<c>{function}:{line}</c>| "
    "{message}"
)

_LOG_LEVEL = "INFO"


def _default_filter(record: "LoguruRecord"):
    def abstract_filter(error_no: int) -> bool:
        config_no = (
            _logger.level(_LOG_LEVEL).no if isinstance(_LOG_LEVEL, str) else _LOG_LEVEL
        )
        return error_no >= config_no

    return abstract_filter(record["level"].no)


_logger.add(
    sys.stdout,
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
    _LOG_LEVEL = level
    _logger.remove()
    _logger.add(
        sys.stdout,
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
        sys.stdout,
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
        self.set_log_level = _set_log_level
        self.set_log_format = _set_log_format
        # self.on_log = _on_log


logger: _Logger = _logger  # type: ignore
logger.set_log_level = _set_log_level
logger.set_log_format = _set_log_format
# logger.on_log = _on_log
