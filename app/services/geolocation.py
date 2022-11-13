import aiohttp

from app.core.config import API_KEY_POSITIONSTACK
from app.models.geolocation import Geolocation

GEO_PROVIDER_API = "http://api.positionstack.com/"


async def get_coordinates_by_query(query: str) -> list[Geolocation]:
    async with aiohttp.ClientSession(base_url=GEO_PROVIDER_API) as client:
        async with client.get("/v1/forward", params={"access_key": API_KEY_POSITIONSTACK, "query": query}) as response:
            if not response.ok:
                raise ValueError("Provider temporary unavailable")
            locations = (await response.json()).get("data", [])
            return [Geolocation.parse_obj(loc) for loc in locations]
