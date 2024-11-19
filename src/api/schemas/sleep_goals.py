from time import time

from src.api.schemas.base import BaseSchema


class SleepGoalCreateRequest(BaseSchema):
    sleep_start: time
    sleep_end: time
