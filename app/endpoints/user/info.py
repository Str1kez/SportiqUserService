from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserExists, UserNotFound
from app.schema import Token, User, UserUpdate
from app.tools import get_token_url, move_to_blacklist
from app.usecase import get_user_by_id, update_user
from app.usecase.token import get_validated_access_token


router = APIRouter(tags=["User"], prefix="/info")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_token_url())


@router.get("", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_info(
    token: Token = Depends(get_validated_access_token), session: AsyncSession = Depends(get_session)
):
    try:
        user_db = await get_user_by_id(token.user, session)
    except (IntegrityError, NoResultFound):
        await move_to_blacklist(token.user, "user")
        raise UserNotFound
    return User.from_orm(user_db)


@router.patch("", response_model=User, status_code=status.HTTP_200_OK)
async def update_user_info(
    user_data: UserUpdate,
    token: Token = Depends(get_validated_access_token),
    session: AsyncSession = Depends(get_session),
):
    try:
        user_db = await update_user(user_data, token, session)
    except NoResultFound:
        await move_to_blacklist(token.user, "user")
        raise UserNotFound
    except IntegrityError as err:
        raise UserExists.factory(str(err))
    return User.from_orm(user_db)
