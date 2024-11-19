from time import time

from src.api.schemas.base import BaseSchema


class SleepGoalSchema(BaseSchema):
    user_id: int
    sleep_start: time
    sleep_end: time


class SleepGoalCreateRequest(BaseSchema):
    sleep_start: time
    sleep_end: time
