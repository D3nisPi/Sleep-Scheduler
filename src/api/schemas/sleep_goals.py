from datetime import time

from pydantic import Field

from src.api.schemas.base import BaseSchema


class SleepGoalSchema(BaseSchema):
    user_id: int
    sleep_start: time
    sleep_end: time


class SleepGoalCreateRequest(BaseSchema):
    sleep_start: time
    sleep_end: time


class SleepGoalReadResponse(BaseSchema):
    sleep_start: time
    sleep_end: time


class SleepGoalUpdateRequest(BaseSchema):
    sleep_start: time = Field(None)
    sleep_end: time = Field(None)
