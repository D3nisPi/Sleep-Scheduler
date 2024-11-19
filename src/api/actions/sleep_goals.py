from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dals.sleep_goals import SleepGoalDAL
from src.api.schemas.sleep_goals import SleepGoalCreateRequest, SleepGoalSchema


async def get_sleep_goal_by_user_id(user_id: int, session: AsyncSession) -> SleepGoalSchema | None:
    async with session.begin():
        sleep_goal_dal = SleepGoalDAL(session)
        sleep_goal = await sleep_goal_dal.get_sleep_goal_by_user_id(user_id)
        if sleep_goal is None:
            return
        return SleepGoalSchema.model_validate(sleep_goal)


async def create_new_user(user_id, body: SleepGoalCreateRequest, session: AsyncSession) -> None:
    async with session.begin():
        sleep_goal_dal = SleepGoalDAL(session)
        await sleep_goal_dal.create_sleep_goal(user_id, body.sleep_start, body.sleep_end)


async def delete_user_by_id(user_id: int, session: AsyncSession) -> bool:
    async with session.begin():
        sleep_goal_dal = SleepGoalDAL(session)
        deleted = await sleep_goal_dal.delete_sleep_goal_by_id(user_id)
        return deleted


async def update_user_by_id(user_id: int, updated_params: dict, session: AsyncSession) -> bool:
    async with session.begin():
        sleep_goal_dal = SleepGoalDAL(session)
        updated = await sleep_goal_dal.update_sleep_goal_by_user_id(user_id, **updated_params)
        return updated
