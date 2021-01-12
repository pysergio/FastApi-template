from fastapi import FastAPI
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app.core.config import MONGO_DATABASE_URL as DATABASE_URL


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to {0}", repr(DATABASE_URL))

    app.state.mongoClient = AsyncIOMotorClient(str(DATABASE_URL))
    options = {"async": True}
    app.state.mongoClient.fsync(**options)

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to {0} database", repr(DATABASE_URL))

    app.state.mongoClient.close()

    logger.info("Connection closed")
