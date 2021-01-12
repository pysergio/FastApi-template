import logging
import sys
from typing import List

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler

API_PREFIX = ""

JWT_TOKEN_PREFIX = "Token"  # noqa: S105

config = Config(".env")

VERSION = config("VERSION", cast=str, default="-.-.-")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

MONGO_DATABASE_URL: DatabaseURL = config("MONGO_DB_CONNECTION", cast=DatabaseURL)
PG_DATABASE_URL: DatabaseURL = config("PG_DB_CONNECTION", cast=DatabaseURL)

MAX_CONNECTIONS_COUNT: int = config("PG_MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("PG_MIN_CONNECTIONS_COUNT", cast=int, default=10)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
PROJECT_NAME: str = config("PROJECT_NAME", default="Darqube CRM")

ALLOWED_HOSTS: List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="")

# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
