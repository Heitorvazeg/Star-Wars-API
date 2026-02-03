from fastapi import APIRouter

from app.api import endpoint

router = APIRouter(prefix="/api/v1")

router.include_router(endpoint.router, prefix="/")
