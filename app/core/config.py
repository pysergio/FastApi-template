import logging
import sys

from loguru import logger
from starlette.config import Config

from app.core.logging import InterceptHandler

config = Config(".env")

VERSION = config("VERSION", cast=str, default="0.0.1")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
API_PREFIX: str = "/weather"
PROJECT_NAME: str = config("PROJECT_NAME", default="Weather api")

CONNECTION_REDIS: str = config("CONNECTION_REDIS", default="redis://redis:6379/?db=0")

API_KEY_POSITIONSTACK: str = config("API_KEY_POSITIONSTACK", default="e7ceb1186afb8e5070a5e33a34812f16")
# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
