from typing import Optional

from pydantic import BaseModel, Field


class Geolocation(BaseModel):
    latitude: float = Field(example=38.897473)
    longitude: float = Field(example=-77.036548)
    type: Optional[str] = Field(example="address")
    name: Optional[str] = Field(example="1600 Pennsylvania Avenue Northwest")
    number: Optional[str] = Field(example="1600")
    postal_code: Optional[str] = Field(example="20500")
    street: Optional[str] = Field(example="Pennsylvania Avenue Northwest")
    confidence: Optional[str] = Field(example=1)
    region: Optional[str] = Field(example="District of Columbia")
    region_code: Optional[str] = Field(example="DC")
    county: Optional[str] = Field(example="District of Columbia")
    locality: Optional[str] = Field(example="Washington")
    administrative_area: Optional[str]
    neighbourhood: Optional[str] = Field(example="White House Grounds")
    country: Optional[str] = Field(example="United States")
    country_code: Optional[str] = Field(example="USA")
    continent: Optional[str] = Field(example="North America")
    label: Optional[str] = Field(example="1600 Pennsylvania Avenue Northwest")
