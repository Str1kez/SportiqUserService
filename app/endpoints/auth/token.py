from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.config import JWTSettings
from app.db.storage import Storage
from app.usecase.token import get_secret_key


router = APIRouter(tags=["Auth"], prefix="/token")


@router.post("/refresh")  # TODO: Замена на новый класс
async def refresh(Authorize: AuthJWT = Depends(), secret_key: str = Depends(get_secret_key)):
    pass
