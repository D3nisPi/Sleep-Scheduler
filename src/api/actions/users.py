from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dals.users import UsersDAL
from src.core.models.users import UsersORM


async def get_user_by_id(user_id: int, session: AsyncSession) -> UsersORM | None:
    async with session.begin():
        user_dal = UsersDAL(session)
        user = await user_dal.get_user_by_id(user_id)
        return user


async def get_user_by_username(username: str, session: AsyncSession) -> UsersORM | None:
    async with session.begin():
        user_dal = UsersDAL(session)
        user = await user_dal.get_user_by_username(username)
        return user


async def update_user_refresh_token_by_id(user_id: int, jti: str | None, session: AsyncSession) -> None:
    async with session.begin():
        user_dal = UsersDAL(session)
        user = await user_dal.update_user_refresh_token_by_id(user_id, jti)
        return user
