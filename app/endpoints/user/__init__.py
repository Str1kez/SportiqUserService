from fastapi import APIRouter

from app.endpoints.user.delete import router as delete_router
from app.endpoints.user.info import router as info_router


router = APIRouter(tags=["User"], prefix="/user")
router.include_router(info_router)
router.include_router(delete_router)


__all__ = ["router"]
