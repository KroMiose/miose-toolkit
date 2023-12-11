import io
import re
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..src import logger
else:
    from src import logger


def test_logger():
    logger.set_log_level("DEBUG")
    logger.debug("This is a debug message.")
    logger.set_log_level("INFO")
    logger.info("Now the log level is INFO then set to DEBUG.")
    logger.debug("This message will not be printed.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

    logger.set_log_format(
        "<g>{time:MM-DD HH:mm:ss}</g> "
        "[<lvl>{level}</lvl>] "
        "<c><u>{name}</u></c> | "
        "<c>{function}:{line}</c>| "
        "{message}",
    )
    logger.info("This is a new format message.")

    # @logger.on_log()
    # def _(record):
    #     print("on_log:", record)

    # logger.info("This message will be printed twice.")


def main():
    test_logger()
