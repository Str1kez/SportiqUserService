from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserNotFound
from app.schema import Token
from app.tools import get_token_url, move_to_blacklist
from app.usecase import delete_user
from app.usecase.token import get_validated_access_token


router = APIRouter(tags=["User"], prefix="/account")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_token_url())


@router.delete("", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(
    token: Token = Depends(get_validated_access_token), session: AsyncSession = Depends(get_session)
):
    try:
        await delete_user(token.user, session)
    except NoResultFound:
        await move_to_blacklist(token.user, "user")
        raise UserNotFound
    await move_to_blacklist(token.user, "user")
