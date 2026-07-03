"""V1 API Packages."""

from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.videos import router as videos_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(videos_router, prefix="/videos", tags=["videos"])
