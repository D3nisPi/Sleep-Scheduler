from datetime import date, time

from sqlalchemy import select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.sleep_notes import SleepNotesORM


class SleepNoteDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_sleep_note_by_id_and_user_id(self, note_id: int, user_id: int) -> SleepNotesORM | None:
        query = (
            select(SleepNotesORM)
            .where(and_(SleepNotesORM.id == note_id, SleepNotesORM.user_id == user_id))
        )
        result = await self.session.execute(query)
        sleep_note = result.scalars().first()
        return sleep_note

    async def get_sleep_note_by_date_and_user_id(self, note_date: date, user_id: int) -> SleepNotesORM | None:
        query = (
            select(SleepNotesORM)
            .where(and_(SleepNotesORM.note_date == note_date, SleepNotesORM.user_id == user_id))
        )
        result = await self.session.execute(query)
        sleep_note = result.scalars().first()
        return sleep_note

    async def create_sleep_note(self,
                                note_date: date,
                                sleep_start: time,
                                sleep_end: time,
                                rating: int | None,
                                comment: str | None,
                                user_id: int
                                ) -> None:
        new_sleep_note = SleepNotesORM(
            note_date=note_date,
            sleep_start=sleep_start,
            sleep_end=sleep_end,
            rating=rating,
            comment=comment,
            user_id=user_id
        )
        self.session.add(new_sleep_note)
        await self.session.commit()

    async def delete_sleep_note_by_id_and_user_id(self, note_id: int, user_id: int) -> bool:
        query = (
            delete(SleepNotesORM)
            .where(and_(SleepNotesORM.id == note_id, SleepNotesORM.user_id == user_id))
            .returning(SleepNotesORM.user_id)
        )
        res = await self.session.execute(query)
        await self.session.commit()

        return bool(res.scalars().first())

    async def delete_sleep_note_by_date_and_user_id(self, note_date: date, user_id: int) -> bool:
        query = (
            delete(SleepNotesORM)
            .where(and_(SleepNotesORM.note_date == note_date, SleepNotesORM.user_id == user_id))
            .returning(SleepNotesORM.user_id)
        )
        res = await self.session.execute(query)
        await self.session.commit()

        return bool(res.scalars().first())

    async def update_sleep_note_by_id_and_user_id(self, note_id: int, user_id: int, updated_params: dict) -> bool:
        query = (
            update(SleepNotesORM)
            .where(and_(SleepNotesORM.id == note_id, SleepNotesORM.user_id == user_id))
            .values(**updated_params)
            .returning(SleepNotesORM.user_id)
        )
        res = await self.session.execute(query)
        await self.session.commit()
        return bool(res.scalars().first())

    async def update_sleep_note_by_date_and_user_id(self, note_date: date, user_id: int, updated_params: dict) -> bool:
        query = (
            update(SleepNotesORM)
            .where(and_(SleepNotesORM.note_date == note_date, SleepNotesORM.user_id == user_id))
            .values(**updated_params)
            .returning(SleepNotesORM.user_id)
        )
        res = await self.session.execute(query)
        await self.session.commit()
        return bool(res.scalars().first())
