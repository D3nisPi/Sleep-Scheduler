from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dals.sleep_notes import SleepNoteDAL
from src.api.schemas.sleep_notes import SleepNoteSchema, SleepNoteCreateRequest


async def get_sleep_note_by_id_and_user_id(note_id: int,
                                           user_id: int,
                                           session: AsyncSession
                                           ) -> SleepNoteSchema | None:
    async with session.begin():
        sleep_note_dal = SleepNoteDAL(session)
        sleep_note = await sleep_note_dal.get_sleep_note_by_id_and_user_id(note_id, user_id)
        if sleep_note is None:
            return
        return SleepNoteSchema.model_validate(sleep_note)


async def get_sleep_note_by_date_and_user_id(note_date: date,
                                             user_id: int,
                                             session: AsyncSession
                                             ) -> SleepNoteSchema | None:
    async with session.begin():
        sleep_note_dal = SleepNoteDAL(session)
        sleep_note = await sleep_note_dal.get_sleep_note_by_date_and_user_id(note_date, user_id)
        if sleep_note is None:
            return
        return SleepNoteSchema.model_validate(sleep_note)


async def create_new_sleep_note(user_id, body: SleepNoteCreateRequest, session: AsyncSession) -> None:
    async with session.begin():
        sleep_note_dal = SleepNoteDAL(session)
        await sleep_note_dal.create_sleep_note(
            body.note_date,
            body.sleep_start,
            body.sleep_end,
            body.rating,
            body.comment,
            user_id
        )


async def delete_sleep_note_by_id_and_user_id(note_id: int, user_id: int, session: AsyncSession) -> bool:
    async with session.begin():
        sleep_note_dal = SleepNoteDAL(session)
        deleted = await sleep_note_dal.delete_sleep_note_by_id_and_user_id(note_id, user_id)
        return deleted


async def delete_sleep_note_by_date_and_user_id(note_date: date, user_id: int, session: AsyncSession) -> bool:
    async with session.begin():
        sleep_note_dal = SleepNoteDAL(session)
        deleted = await sleep_note_dal.delete_sleep_note_by_date_and_user_id(note_date, user_id)
        return deleted


async def update_sleep_note_by_id_and_user_id(note_id: int,
                                              user_id: int,
                                              updated_params: dict,
                                              session: AsyncSession
                                              ) -> bool:
    async with session.begin():
        sleep_note_dal = SleepNoteDAL(session)
        updated = await sleep_note_dal.update_sleep_note_by_id_and_user_id(note_id, user_id, updated_params)
        return updated


async def update_sleep_note_by_date_and_user_id(note_date: date,
                                                user_id: int,
                                                updated_params: dict,
                                                session: AsyncSession
                                                ) -> bool:
    async with session.begin():
        sleep_note_dal = SleepNoteDAL(session)
        updated = await sleep_note_dal.update_sleep_note_by_date_and_user_id(note_date, user_id, updated_params)
        return updated
