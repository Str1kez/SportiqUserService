from fastapi import APIRouter

from app.endpoints.user.info import router as info_router


router = APIRouter(tags=["User"], prefix="/user")
router.include_router(info_router)


__all__ = ["router"]
