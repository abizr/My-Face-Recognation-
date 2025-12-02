import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.log(level, record.getMessage())


def setup_logging() -> None:
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.add("logs/app.log", rotation="10 MB", retention=5, enqueue=True, backtrace=True, diagnose=False)
