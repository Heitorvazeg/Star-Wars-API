import pytest
import httpx
from unittest.mock import MagicMock
from app.services.swapi import SwapiService

BASE_URL = "https://swapi.dev/api"

@pytest.fixture
def mock_cache():
    cache = MagicMock()
    cache.get.return_value = None
    return cache

@pytest.fixture
def swapi_service(mock_cache):
    service = SwapiService(url=BASE_URL)
    service.Cache = mock_cache
    return service

@pytest.mark.asyncio
async def test_fetch_with_filters_and_sorting(swapi_service, httpx_mock):
    """Testa o fluxo completo usando filtros permitidos no model."""
    
    api_response = {
        "results": [
            {"name": "Luke Skywalker", "eye_color": "blue", "height": "172"},
            {"name": "C-3PO", "eye_color": "yellow", "height": "167"},
            {"name": "Darth Vader", "eye_color": "yellow", "height": "202"},
        ]
    }
    
    # O service envia ?page=1 por padrão
    httpx_mock.add_response(
        url=f"{BASE_URL}/people/?page=1",
        json=api_response,
        method="GET"
    )

    # 'eye_color' está no RESOURCE_VALID_FILTERS, então não será descartado
    # 'sort_by' é extraído via pop() antes do filtro de 'allowedFilters'
    params = {"eye_color": "yellow", "sort_by": "height"}
    results = await swapi_service.fetch("people", params)

    # Asserts
    # Deve filtrar apenas os de olho amarelo (C-3PO e Vader)
    assert len(results) == 2
    # Ordenação: 167 (C-3PO) vem antes de 202 (Vader)
    assert results[0]["name"] == "C-3PO"
    assert results[1]["name"] == "Darth Vader"
    
    assert swapi_service.Cache.set.called

@pytest.mark.asyncio
async def test_fetch_cache_hit(swapi_service, httpx_mock):
    mock_data = [{"name": "Yoda"}]
    swapi_service.Cache.get.return_value = mock_data

    # A chave do cache deve ser gerada consistentemente
    results = await swapi_service.fetch("people", {"search": "yoda"})

    assert results == mock_data
    assert len(httpx_mock.get_requests()) == 0

@pytest.mark.asyncio
async def test_fetch_call_direct(swapi_service, httpx_mock):
    httpx_mock.add_response(url=f"{BASE_URL}/planets/", json={"count": 60})

    async with httpx.AsyncClient() as client:
        result = await swapi_service.fetchCall(client, "planets", {})

    assert result["count"] == 60
