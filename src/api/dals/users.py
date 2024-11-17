from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.users import UsersORM


class UsersDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> UsersORM | None:
        query = (
            select(UsersORM)
            .where(UsersORM.id == user_id)
        )
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user

    async def get_user_by_username(self, username: str) -> UsersORM | None:
        query = (
            select(UsersORM)
            .where(UsersORM.username == username)
        )
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user

    async def create_user(self, username: str, display_name: str, password_hash: str) -> bool:
        new_user = UsersORM(
            username=username,
            display_name=display_name,
            password_hash=password_hash,
            refresh_token_id=None
        )
        try:
            self.session.add(new_user)
            await self.session.commit()
            return True
        except IntegrityError:
            await self.session.rollback()
            return False

    async def delete_user_by_id(self, user_id: int) -> bool:
        query = (
            delete(UsersORM)
            .where(UsersORM.id == user_id)
            .returning(UsersORM.id)
        )
        res = await self.session.execute(query)
        await self.session.commit()

        return bool(res.scalars().first())

    async def update_user_by_id(self, user_id: int, **updated_params) -> bool:
        query = (
            update(UsersORM)
            .where(UsersORM.id == user_id)
            .values(updated_params)
            .returning(UsersORM.id)
        )
        res = await self.session.execute(query)
        await self.session.commit()
        return bool(res.scalars().first())

    async def update_user_refresh_token_by_id(self, user_id: int, jti: str | None) -> None:
        query = (
            update(UsersORM)
            .where(UsersORM.id == user_id)
            .values(refresh_token_id=jti)
        )

        await self.session.execute(query)
        await self.session.commit()
