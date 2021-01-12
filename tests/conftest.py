from os import environ, getenv

import docker as libdocker
import pytest
from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient

from app.models.domain.users import UserInDB
from app.services import jwt

POSTGRES_DOCKER_IMAGE = "postgres:11.4-alpine"

USE_LOCAL_DB = getenv("USE_LOCAL_DB_FOR_TEST", False)


@pytest.fixture(scope="session")
def docker() -> libdocker.APIClient:
    with libdocker.APIClient(version="auto") as client:
        yield client


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
def pool(initialized_app: FastAPI) -> Pool:
    return initialized_app.state.pool


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def authorization_prefix() -> str:
    from app.core.config import JWT_TOKEN_PREFIX

    return JWT_TOKEN_PREFIX


@pytest.fixture
def token(test_user: UserInDB) -> str:
    return jwt.create_access_token_for_user(test_user, environ["SECRET_KEY"])
