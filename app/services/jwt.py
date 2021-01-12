from datetime import datetime, timedelta
from typing import Dict

import jwt
from pydantic import ValidationError

from app.core import config
from app.models.schemas.auth.auth import User
from app.models.schemas.jwt import JWTMeta, JWTUser

JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week


def create_jwt_token(*, jwt_content: Dict[str, str], secret_key: str, expires_delta: timedelta) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).dict())
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM).decode()


def create_access_token_for_user(user: User, secret_key: str = config.SECRET_KEY, **kwargs) -> str:
    return create_jwt_token(
        jwt_content=JWTUser(uid=user.uid, email=user.email, **kwargs).dict(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def get_uid_from_token(token: str, secret_key: str = config.SECRET_KEY) -> str:
    try:
        return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM])).uid
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
