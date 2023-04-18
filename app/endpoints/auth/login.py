from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserNotFound
from app.schema import CreatedTokens, Login
from app.usecase import create_tokens, get_active_user


router = APIRouter(tags=["Auth"], prefix="/login")


@router.post("", response_model=CreatedTokens, status_code=status.HTTP_200_OK)
async def login(
    credentials: Login,
    session: AsyncSession = Depends(get_session),
):
    try:
        user = await get_active_user(credentials, session)
    except NoResultFound:
        raise UserNotFound
    return await create_tokens(user._id)
