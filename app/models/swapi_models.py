from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# SwapiFilters to getting the query params
class SwapiFilters(BaseModel):
    search: Optional[str] = None
    page: Optional[int] = Field(1, ge=1)
    sort_by: Optional[str] = None
    eye_color: Optional[str] = None
    climate: Optional[str] = None
    director: Optional[str] = None
    model: Optional[str] = None


# Limits the resource allowed on the controller
class SwapiResources(str, Enum):
    people = "people"
    planets = "planets"
    starships = "starships"
    films = "films"


# For each resource limits the allowed filter
RESOURCE_VALID_FILTERS = {
    "people": ["search", "page", "sort", "eye_color"],
    "planets": ["search", "page", "sort", "climate"],
    "films": ["search", "page", "sort", "director"],
    "starships": ["search", "page", "sort", "model"],
}
