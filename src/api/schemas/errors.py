from typing import List, Literal

from src.api.schemas.base import BaseSchema


class CommonErrorResponse(BaseSchema):
    detail: str


class DatabaseErrorDetail(BaseSchema):
    table: str
    fields: list[str]
    error_type: Literal[
        "unique_constraint",
        "check_constraint",
        "primary_key_constraint",
        "foreign_key_constraint",
        "unknown"
    ]


class DatabaseErrorResponse(BaseSchema):
    detail: List[DatabaseErrorDetail]
