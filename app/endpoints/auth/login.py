from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions import UserNotFound
from app.schema import Login
from app.usecase import get_user


router = APIRouter(tags=["Auth"], prefix="/login")


@router.post("", response_class=Response, status_code=status.HTTP_200_OK)
async def login(credentials: Login, session: AsyncSession = Depends(get_session)):
    try:
        user = await get_user(credentials, session)
    except NoResultFound:
        raise UserNotFound
    print(user)
