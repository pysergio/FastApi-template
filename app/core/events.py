from typing import Any, Callable

from aioredis import Redis
from atomcache import Cache
from fastapi import FastAPI
from loguru import logger

from app.core.config import CONNECTION_REDIS


def create_start_app_handler(app: FastAPI) -> Callable[[], Any]:
    async def start_app() -> None:
        await Cache.init(app=app, cache_client=Redis.from_url(CONNECTION_REDIS))

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable[[], Any]:
    @logger.catch
    async def stop_app() -> None:
        await Cache.backend.close()

    return stop_app
