from pathlib import Path
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

    # 测试日志输出到文件
    temp_dir = Path("./temp")
    logger.set_log_output(temp_dir / "test_logger.log", True)
    logger.info("(Logger Test) This message will be printed to file.")
    logger.set_log_output(temp_dir / "test_logger.log", False)
    logger.info("(Logger Test) This message will not be printed to console.")
    assert (temp_dir / "test_logger.log").exists()
    with (temp_dir / "test_logger.log").open("r") as file:
        assert "(Logger Test) This message will be printed to file." in file.read()
        assert (
            "(Logger Test) This message will not be printed to console."
            not in file.read()
        )
        file.close()
    logger.unset_log_output()

    logger.success("(Logger Test) This is a success message.")

    (temp_dir / "test_logger.log").unlink(True)


def main():
    test_logger()
