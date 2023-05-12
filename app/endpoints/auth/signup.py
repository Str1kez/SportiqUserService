from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserExists
from app.schema import CreatedTokens, SignUp
from app.usecase import create_user
from app.usecase.token import create_token


router = APIRouter(tags=["Auth"], prefix="/signup")


@router.post("", response_model=CreatedTokens, status_code=status.HTTP_201_CREATED)
async def signup(
    response: Response,
    credentials: SignUp,
    session: AsyncSession = Depends(get_session),
) -> CreatedTokens:
    try:
        user = await create_user(credentials, session)
    except IntegrityError as err:
        raise UserExists.factory(str(err))
    access_token = CreatedTokens(access_token=await create_token(user._id, "access"))
    refresh_token = await create_token(user._id, "refresh")
    response.set_cookie("refreshToken", refresh_token, httponly=True, domain="api.sportiq.org")
    return access_token
