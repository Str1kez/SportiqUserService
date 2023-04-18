from fastapi import APIRouter, Depends

from app.config import JWTSettings
from app.db.storage import Storage


router = APIRouter(tags=["Auth"], prefix="/token")


@router.post("/refresh")  # TODO: Замена на новый класс
async def refresh():
    pass
