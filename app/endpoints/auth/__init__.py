from fastapi import APIRouter

from app.endpoints.auth.login import router as login_router
from app.endpoints.auth.signup import router as signup_router
from app.endpoints.auth.token import router as token_router


router = APIRouter(tags=["Auth"], prefix="/auth")
router.include_router(login_router)
router.include_router(signup_router)
router.include_router(token_router)


__all__ = ["router"]
