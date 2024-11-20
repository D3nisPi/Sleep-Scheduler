from datetime import time

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.sleep_goals import SleepGoalsORM


class SleepGoalDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_sleep_goal_by_user_id(self, user_id: int) -> SleepGoalsORM | None:
        query = (
            select(SleepGoalsORM)
            .where(SleepGoalsORM.user_id == user_id)
        )
        result = await self.session.execute(query)
        sleep_goal = result.scalars().first()
        return sleep_goal

    async def create_sleep_goal(self, user_id: str, sleep_start: time, sleep_end: time) -> None:
        new_sleep_goal = SleepGoalsORM(
            user_id=user_id,
            sleep_start=sleep_start,
            sleep_end=sleep_end
        )
        self.session.add(new_sleep_goal)
        await self.session.commit()

    async def delete_sleep_goal_by_id(self, user_id: int) -> bool:
        query = (
            delete(SleepGoalsORM)
            .where(SleepGoalsORM.user_id == user_id)
            .returning(SleepGoalsORM.user_id)
        )
        res = await self.session.execute(query)
        await self.session.commit()

        return bool(res.scalars().first())

    async def update_sleep_goal_by_user_id(self, user_id: int, updated_params: dict) -> bool:
        query = (
            update(SleepGoalsORM)
            .where(SleepGoalsORM.user_id == user_id)
            .values(**updated_params)
            .returning(SleepGoalsORM.user_id)
        )
        res = await self.session.execute(query)
        await self.session.commit()
        return bool(res.scalars().first())
