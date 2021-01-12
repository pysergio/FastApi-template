import asyncpg
from fastapi import FastAPI
from loguru import logger

from app.core.config import (
    MAX_CONNECTIONS_COUNT,
    MIN_CONNECTIONS_COUNT,
    PG_DATABASE_URL as DATABASE_URL,
)


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to {0}", repr(DATABASE_URL))

    app.state.pgPool = await asyncpg.create_pool(
        str(DATABASE_URL),
        min_size=MIN_CONNECTIONS_COUNT,
        max_size=MAX_CONNECTIONS_COUNT,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    # await app.state.pgPool.close()

    logger.info("Connection closed")
