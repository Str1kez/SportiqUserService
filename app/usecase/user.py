from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schema import Login, UserDTO


async def create_user(user_data: UserDTO, session: AsyncSession) -> None:
    user = user_data.to_dict_with_hashed_password()
    await session.execute(insert(User), [user])
    await session.commit()


async def get_user(user_data: Login, session: AsyncSession) -> UserDTO:
    user = user_data.to_orm()
    query = select(User).where(User.username == user["username"])
    result = await session.execute(query)
    user_dto = UserDTO.from_orm(result.scalar_one())
    user_data.validate_password(user_dto.password.get_secret_value())
    return user_dto
