import aiohttp
from fastapi import APIRouter, HTTPException, Response
from loguru import logger
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

from app.core import config
from app.models.schemas.auth.auth import User
from app.services import jwt

router = APIRouter()


class Credentials(BaseModel):
    email: str
    password: str


@router.get("/google_oauth2/callback", response_model=User, name="auth:get-user-by_google")
async def google_auth(provider: str, token: str, response: Response) -> User:
    url = f"{config.CRM_URL}/google_oauth2/callback"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=dict(provider=provider, token=token)) as resp:
            json_resp = await resp.json()
            if resp.status != HTTP_200_OK:
                raise HTTPException(status_code=resp.status, detail=json_resp)
            access_token, client = resp.header["access_token"], resp.header["client"]

    user = User(**json_resp)
    auth_token = jwt.create_access_token_for_user(user, access_token=access_token, client=client)
    response.set_cookie(key=config.AUTH_COOKIES_NAME, value=auth_token, **config.AUTH_COOKIES_CONF)
    return user


@router.post("/sign_in", response_model=User, name="auth:get-user-by_credentials")
async def credential_auth(credentials: Credentials, response: Response) -> User:
    url = f"{config.CRM_URL}/sign_in"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=credentials.dict()) as resp:
            json_resp = await resp.json()
            logger.error(resp.status)
            if resp.status != HTTP_200_OK:
                raise HTTPException(status_code=resp.status, detail=json_resp)
            access_token, client = resp.header["access_token"], resp.header["client"]

    user = User(**json_resp)
    auth_token = jwt.create_access_token_for_user(user, access_token=access_token, client=client)
    response.set_cookie(key=config.AUTH_COOKIES_NAME, value=auth_token, **config.AUTH_COOKIES_CONF)
    return user
