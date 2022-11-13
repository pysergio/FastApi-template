import aiohttp

from app.models.wether import Weather

WHETHER_PROVIDER_API = "https://fcc-weather-api.glitch.me/"


async def get_weather_by_coordinates(latitude: float, longitude: float) -> Weather:
    async with aiohttp.ClientSession(base_url=WHETHER_PROVIDER_API) as client:
        async with client.get("/api/current", params={"lat": latitude, "lon": longitude}) as response:
            if not response.ok:
                raise ValueError("Provider temporary unavailable")
            return Weather.parse_obj(await response.json())
