from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import DBError
from app.schema import CreatedTokens, UserDTO
from app.usecase import create_tokens, create_user, get_secret_key


router = APIRouter(tags=["Auth"], prefix="/signup")


@router.post("", response_model=CreatedTokens, status_code=status.HTTP_201_CREATED)
async def signup(
    credentials: UserDTO,
    session: AsyncSession = Depends(get_session),
    secret_key: str = Depends(get_secret_key),
    Authorize: AuthJWT = Depends(),  # TODO: Замена на новый класс
):
    try:
        await create_user(credentials, session)
    except IntegrityError as err:
        raise DBError(detail=str(err))
    return create_tokens(credentials, Authorize, secret_key)
