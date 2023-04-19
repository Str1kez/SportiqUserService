from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schema import Login, SignUp
from app.schema.token import Token
from app.schema.user import UserUpdate


async def create_user(user_data: SignUp, session: AsyncSession) -> User:
    user = user_data.to_dict_with_hashed_password()
    result = await session.execute(insert(User).returning(User), [user])
    user_db = result.scalar_one()
    await session.commit()
    return user_db


async def get_active_user(user_data: Login, session: AsyncSession) -> User:
    query = select(User).where(User.username == user_data.username).where(User.is_active == True)
    result = await session.execute(query)
    user_db = result.scalar_one()
    user_data.validate_password(user_db.password)
    return user_db


async def get_user_by_id(user_id: str, session: AsyncSession) -> User:
    query = select(User).where(User._id == user_id).where(User.is_active == True)
    result = await session.execute(query)
    user_db = result.scalar_one()
    return user_db


async def update_user(user: UserUpdate, token: Token, session: AsyncSession) -> User:
    query = (
        update(User)
        .where(User._id == token.user)
        .where(User.is_active == True)
        .values(**user.prepared_dict())
        .returning(User)
    )
    request = await session.execute(query)
    user_db = request.scalar_one()
    await session.commit()
    return user_db


async def delete_user(user_id: str, session: AsyncSession) -> None:
    query = update(User).where(User._id == user_id).where(User.is_active == True).values({"is_active": False})
    await session.execute(query)
    await session.commit()
