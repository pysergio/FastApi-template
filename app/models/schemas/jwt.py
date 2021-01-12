from datetime import datetime

from pydantic import BaseModel, validator


class JWTMeta(BaseModel):
    exp: datetime
    sub: str

    @validator("exp", pre=True)
    def default_datetime(cls, expire: datetime) -> datetime:  # noqa: N805
        return expire or datetime.utcnow()


class JWTUser(JWTMeta):
    uid: int
    email: str
