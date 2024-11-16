from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.users import UsersOrm


class UsersDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str) -> UsersOrm | None:
        query = (
            select(UsersOrm)
            .where(UsersOrm.username == username)
        )
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user
