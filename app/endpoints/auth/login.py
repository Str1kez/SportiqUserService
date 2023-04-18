from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserNotFound
from app.schema import CreatedTokens, Login
from app.usecase import get_active_user
from app.usecase.token import create_tokens


router = APIRouter(tags=["Auth"], prefix="/login")


@router.post("", response_model=CreatedTokens, status_code=status.HTTP_200_OK)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> CreatedTokens:
    try:
        user = await get_active_user(Login(username=credentials.username, password=credentials.password), session)
    except NoResultFound:
        raise UserNotFound
    return await create_tokens(user._id)
