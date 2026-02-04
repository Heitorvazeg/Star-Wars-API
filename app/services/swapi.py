import httpx
from core.settings import settings
from app.models.swapi_models import RESOURCE_VALID_FILTERS
from core.cache_in_memory import Cache
import json


class SwapiService:
    """Service to interact with the Star Wars API (SWAPI)."""

    def __init__(self, url: str = settings.SWAPI_URL, ttl: int = 300):
        self.url = url
        self.Cache = Cache(ttl=ttl)

    # Call SWAPI and get data
    async def fetchCall(self, client: httpx.AsyncClient, resource: str, paramsApi):
        response = await client.get(f"{self.url}/{resource}/", params=paramsApi)
        response.raise_for_status()
        data = response.json()

        return data

    async def fetch(self, resource: str, params: dict = None):
        # If there is cached data, returns it
        # Can be implemented as a decorator
        cacheKey = f"{resource}:{json.dumps(params, sort_keys=True)}"
        cachedData = self.Cache.get(cacheKey)
        if cachedData:
            return cachedData

        # RESOURCE_VALID_FILTERS gives filters available to be used on the back
        # Works as a validation to unsuported filters
        allowedFilters = RESOURCE_VALID_FILTERS.get(resource, [])

        cleanParams = {k: v for k, v in params.items() if k in allowedFilters}

        # Create the SWAPI request dict
        search = cleanParams.pop("search", None)
        page = cleanParams.pop("page", 1)
        sortBy = cleanParams.pop("sort_by", None)

        paramsApi: dict = {"page": page}
        if search:
            paramsApi["search"] = search

        if sortBy:
            paramsApi["sort_by"] = sortBy

        # Async call to SWAPI
        async with httpx.AsyncClient() as client:
            data = await self.fetchCall(client, resource, paramsApi)

        results = data.get("results", [])

        # Filtering the data by cleanParams, the filters allowed in the back
        if cleanParams and results:
            results = [
                item
                for item in results
                if all(
                    str(item.get(key, "")).lower() == str(value).lower()
                    for key, value in cleanParams.items()
                )
            ]

        # Sorting by the SortBy param
        if sortBy and results:
            results = sorted(results, key=lambda x: x.get(sortBy, ""), reverse=False)

        # Set the cache data
        self.Cache.set(cacheKey, results)

        return results
