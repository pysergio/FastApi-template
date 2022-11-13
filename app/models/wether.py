from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, HttpUrl, root_validator, validator


class Coordinates(BaseModel):
    lon: float
    lat: float


class WeatherDescription(BaseModel):
    main: str = Field(example="Drizzle")
    description: str = Field(example="light intensity drizzle")
    icon: Optional[HttpUrl]


class MainReferences(BaseModel):
    temp: float = Field(example=7.62)
    feels_like: Optional[float] = Field(example=5.02)
    temp_min: Optional[float] = Field(example=7.62)
    temp_max: Optional[float] = Field(example=8.12)
    pressure: Optional[int] = Field(example=1031)
    humidity: Optional[int] = Field(example=99)


class Wind(BaseModel):
    speed: float = Field(example=4.12)
    deg: int = Field(example=360)


class Weather(BaseModel):
    coord: Coordinates
    weather: list[WeatherDescription]
    base: str
    main: MainReferences
    visibility: int = Field(example=10000)
    dt: datetime
    location: str = Field(example="London", alias="name")
    country: str = Field(example="UK")
    sunrise: datetime
    sunset: datetime

    @validator("dt", "sunrise", "sunset", pre=True)
    def cast_ts_to_datetime(cls, value: int | datetime) -> datetime:
        if isinstance(value, int):
            value = datetime.fromtimestamp(value)
        return value

    @root_validator(pre=True)
    def replace_country_root(cls, values: dict[str, Any]) -> dict[str, Any]:
        if sys := values.get("sys"):
            values |= sys
        return values
