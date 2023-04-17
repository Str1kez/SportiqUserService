from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserNotFound
from app.schema import CreatedTokens, Login
from app.usecase import create_tokens, get_active_user, get_secret_key


router = APIRouter(tags=["Auth"], prefix="/login")


@router.post("", response_model=CreatedTokens, status_code=status.HTTP_200_OK)
async def login(
    credentials: Login,
    session: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),  # TODO: Замена на новый класс
    secret_key: str = Depends(get_secret_key),
):
    try:
        user = await get_active_user(credentials, session)
    except NoResultFound:
        raise UserNotFound
    return create_tokens(user, Authorize, secret_key)
