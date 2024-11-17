from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dals.users import UsersDAL
from src.api.schemas.users import UserCreateRequest
from src.api.utils.passwords import hash_password
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


async def create_new_user(body: UserCreateRequest, session: AsyncSession) -> None:
    password_hash = hash_password(body.password)

    async with session.begin():
        user_dal = UsersDAL(session)
        await user_dal.create_user(body.username, body.display_name, password_hash)


async def update_user_refresh_token_by_id(user_id: int, jti: str | None, session: AsyncSession) -> None:
    async with session.begin():
        user_dal = UsersDAL(session)
        user = await user_dal.update_user_refresh_token_by_id(user_id, jti)
        return user
