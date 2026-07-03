"""API Packages."""

from fastapi import APIRouter

from src.api.status import router as status_router
from src.api.v1 import router as v1_router

router = APIRouter()

router.include_router(status_router, tags=["Health"])
router.include_router(v1_router, prefix="/v1", tags=["v1"])
