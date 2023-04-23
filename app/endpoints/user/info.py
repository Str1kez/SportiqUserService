from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserExists, UserNotFound
from app.schema import User, UserUpdate
from app.tools import get_token_url, move_to_blacklist
from app.usecase import get_user_by_id, update_user


router = APIRouter(tags=["User"], prefix="/info")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_token_url())


@router.get("", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_info(user_id: str = Header(..., alias="User"), session: AsyncSession = Depends(get_session)) -> User:
    try:
        user_db = await get_user_by_id(user_id, session)
    except (IntegrityError, NoResultFound):
        await move_to_blacklist(user_id, "user")
        raise UserNotFound
    return User.from_orm(user_db)


@router.patch("", response_model=User, status_code=status.HTTP_200_OK)
async def update_user_info(
    user_data: UserUpdate,
    user_id: str = Header(..., alias="User"),
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        user_db = await update_user(user_data, user_id, session)
    except NoResultFound:
        await move_to_blacklist(user_id, "user")
        raise UserNotFound
    except IntegrityError as err:
        raise UserExists.factory(str(err))
    return User.from_orm(user_db)
