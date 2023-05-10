from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserNotFound
from app.schema import CreatedTokens, Login
from app.usecase import get_active_user
from app.usecase.token import create_token


router = APIRouter(tags=["Auth"], prefix="/login")


@router.post("", response_model=CreatedTokens, status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    credentials: Login,
    session: AsyncSession = Depends(get_session),
) -> CreatedTokens:
    try:
        user = await get_active_user(credentials, session)
    except NoResultFound:
        raise UserNotFound
    access_token = CreatedTokens(access_token=await create_token(user._id, "access"))
    refresh_token = await create_token(user._id, "refresh")
    response.set_cookie("refreshToken", refresh_token, httponly=True)
    return access_token
