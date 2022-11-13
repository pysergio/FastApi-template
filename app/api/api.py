from atomcache import Cache
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.models.wether import Weather
from app.resources.strings import LOCATION_DOES_NOT_EXIST_ERROR
from app.services.geolocation import get_coordinates_by_query
from app.services.wetaher_api import get_weather_by_coordinates

router = APIRouter()


@router.get("/location", response_model=Weather)
async def get_weather(where: str = "London", cache: Cache = Depends(Cache(exp=600))) -> Weather:
    await cache.raise_try(where)
    locations = await get_coordinates_by_query(query=where)
    if not locations:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=LOCATION_DOES_NOT_EXIST_ERROR.format(where))
    loc = locations[0]
    return cache.set(
        await get_weather_by_coordinates(latitude=loc.latitude, longitude=loc.longitude),
        cache_id=where,
    )
