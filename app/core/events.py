import asyncio
from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.db.mongo.events import (
    close_db_connection as close_mongo_connection,
    connect_to_db as connect_to_mongo,
)


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await asyncio.gather(
            connect_to_mongo(app),  # connect_to_pg(app)
        )

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        await asyncio.gather(
            close_mongo_connection(app),  # close_pg_connection(app)
        )

    return stop_app
