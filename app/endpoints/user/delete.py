from fastapi import APIRouter, Depends, Header, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserNotFound
from app.tools import get_token_url, move_to_blacklist
from app.usecase import delete_user


router = APIRouter(tags=["User"], prefix="/account")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_token_url())


@router.delete(
    "",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    description="**need to be authenticated by API Gateway**",
)
async def delete_user_account(user_id: str = Header(..., alias="User"), session: AsyncSession = Depends(get_session)):
    try:
        await delete_user(user_id, session)
    except NoResultFound:
        await move_to_blacklist(user_id, "user")
        raise UserNotFound
    await move_to_blacklist(user_id, "user")
