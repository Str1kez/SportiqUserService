from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection.session import get_session
from app.exceptions.db import DBError
from app.schema import UserDTO
from app.usecase.user import create_user


router = APIRouter(tags=["Auth"], prefix="/signup")


@router.post("", response_class=Response, status_code=status.HTTP_201_CREATED)
async def signup(credentials: UserDTO, session: AsyncSession = Depends(get_session)):
    try:
        await create_user(credentials, session)
    except IntegrityError as err:
        raise DBError(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
