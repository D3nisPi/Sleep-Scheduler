from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dals.sleep_goals import SleepGoalDAL
from src.api.schemas.sleep_goals import SleepGoalCreateRequest
from src.core.models.sleep_goals import SleepGoalsORM


async def get_sleep_goal_by_user_id(user_id: int, session: AsyncSession) -> SleepGoalsORM | None:
    async with session.begin():
        user_dal = SleepGoalDAL(session)
        user = await user_dal.get_sleep_goal_by_user_id(user_id)
        return user


async def create_new_user(user_id, body: SleepGoalCreateRequest, session: AsyncSession) -> None:
    async with session.begin():
        user_dal = SleepGoalDAL(session)
        await user_dal.create_sleep_goal(user_id, body.sleep_start, body.sleep_end)


async def delete_user_by_id(user_id: int, session: AsyncSession) -> bool:
    async with session.begin():
        user_dal = SleepGoalDAL(session)
        deleted = await user_dal.delete_sleep_goal_by_id(user_id)
        return deleted


async def update_user_by_id(user_id: int, updated_params: dict, session: AsyncSession) -> bool:
    async with session.begin():
        user_dal = SleepGoalDAL(session)
        updated = await user_dal.update_sleep_goal_by_user_id(user_id, **updated_params)
        return updated
