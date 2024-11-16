from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.users import UsersORM


class UsersDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str) -> UsersORM | None:
        query = (
            select(UsersORM)
            .where(UsersORM.username == username)
        )
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user

    async def update_user_refresh_token_by_id(self, user_id: int, jti: str) -> None:
        query = (
            update(UsersORM)
            .where(UsersORM.id == user_id)
            .values(refresh_token_id=jti)
        )

        await self.session.execute(query)
        await self.session.commit()
