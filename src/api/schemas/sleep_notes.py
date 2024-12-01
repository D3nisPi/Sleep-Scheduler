from datetime import date, time

from pydantic import Field

from src.api.schemas.base import BaseSchema


class SleepNoteSchema(BaseSchema):
    id: int
    note_date: date
    sleep_start: time
    sleep_end: time
    rating: int | None
    comment: str | None
    user_id: int


class SleepNoteCreateRequest(BaseSchema):
    note_date: date
    sleep_start: time
    sleep_end: time
    rating: int | None = Field(..., ge=1, le=5)
    comment: str | None = Field(..., max_length=300)


class SleepNoteReadResponse(BaseSchema):
    id: int
    note_date: date
    sleep_start: time
    sleep_end: time
    rating: int | None
    comment: str | None


class SleepNoteUpdateRequest(BaseSchema):
    note_date: date = Field(None)
    sleep_start: time = Field(None)
    sleep_end: time = Field(None)
    rating: int | None = Field(None, ge=1, le=5)
    comment: str | None = Field(None, max_length=300)
