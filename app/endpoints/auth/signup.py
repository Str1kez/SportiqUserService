from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserExists
from app.schema import CreatedTokens, SignUp
from app.usecase import create_user
from app.usecase.token import create_tokens


router = APIRouter(tags=["Auth"], prefix="/signup")


@router.post("", response_model=CreatedTokens, status_code=status.HTTP_201_CREATED)
async def signup(
    credentials: SignUp,
    session: AsyncSession = Depends(get_session),
) -> CreatedTokens:
    try:
        user = await create_user(credentials, session)
    except IntegrityError as err:
        raise UserExists.factory(str(err))
    return await create_tokens(user._id)
