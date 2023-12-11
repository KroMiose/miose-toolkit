from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..miose_toolkit_logger import logger
else:
    from miose_toolkit_logger import logger


def test_logger():
    logger.set_log_level("DEBUG")
    logger.debug("(Logger Test) This is a debug message.")
    logger.set_log_level("INFO")
    logger.info("(Logger Test) Now the log level is INFO then set to DEBUG.")
    logger.debug("(Logger Test) This message will not be printed.")
    logger.warning("(Logger Test) This is a warning message.")
    logger.error(
        "(Logger Test) This is an error message, but it will not exit the program.",
    )
    logger.critical(
        "(Logger Test) This is a critical message, but now your program is safe. Don't worry.",
    )

    logger.set_log_format(
        "<g>{time:MM-DD HH:mm:ss}</g> "
        "[<lvl>{level}</lvl>] "
        "<c><u>{name}</u></c> | "
        "<c>{function}:{line}</c>| "
        "{message}",
    )
    logger.info("(Logger Test) This is a new format message.")

    # @logger.on_log()
    # def _(record):
    #     print("on_log:", record)

    # logger.info("This message will be printed twice.")

    logger.success("(Logger Test) This is a success message.")


def main():
    test_logger()
