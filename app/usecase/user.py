from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schema import Login, SignUp


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
