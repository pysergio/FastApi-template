from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id_: int = Field(0, alias="id")
    email: str
    first_name: str
    last_name: str
    username: str
    photo: Optional[str]
    city: Optional[str]
    country: Optional[str]
    date_of_birth: Optional[datetime]
