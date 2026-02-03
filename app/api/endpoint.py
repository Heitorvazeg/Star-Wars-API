from fastapi import FastAPI, Depends
from services.swapi import SwapiService, SwapiFilters
from models.swapi_models import SwapiResources

app = FastAPI()
swapi = SwapiService()

# Resource gives what feature of SWAPI do you want
@app.get("starwars/{resource}/")
async def getResources(resource: SwapiResources, params: SwapiFilters = Depends()):
    # Do not allow None params
    paramsDict = params.model_dump(exclude_none=True)

    return await swapi.fetch(resource=resource, params=paramsDict)
