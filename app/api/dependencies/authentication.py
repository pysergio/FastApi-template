from typing import Optional

from aiohttp import ClientSession
from fastapi import HTTPException, Security
from fastapi.security import APIKeyCookie
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import CRM_URL, JWT_TOKEN_PREFIX
from app.db.auth.auth import User
from app.resources import strings

AUTH_COOKIES_NAME: str = "Authorization"
AUTH_COOKIES_CONF = dict(
    secure=True,
)


class RWAPIKeyHeader(APIKeyCookie):
    async def __call__(self, request: requests.Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=strings.AUTHENTICATION_REQUIRED,
            )


def _get_authorization_token(api_key: str = Security(RWAPIKeyHeader(name=AUTH_COOKIES_NAME))) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    return token


async def _check_auth_remote(email: str, client: str, access_token: str) -> User:
    """This method get User based on old authentication mechanism"""
    auth_headers = {"uid": email, "client": client, "access-token": access_token}

    async with ClientSession(headers=auth_headers) as session:
        async with session.get(f"{CRM_URL}/check_auth") as response:
            resp = await response.json()

    if resp["data"]["message"] == "Not authorized":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=strings.AUTHENTICATION_REQUIRED,
        )

    return User(resp)
