from enum import Enum


class ConstraintType(Enum):
    PRIMARY_KEY = "primary_key_constraint"
    UNIQUE = "unique_constraint"
    FOREIGN_KEY = "foreign_key_constraint"
    CHECK = "check_constraint"


class ConstraintInfo:
    def __init__(self, constraint_type: ConstraintType, table: str, fields: list[str]):
        self.type = constraint_type
        self.table = table
        self.fields = fields


constraints = {
    "pk_users_id": ConstraintInfo(
        ConstraintType.PRIMARY_KEY,
        "users",
        ["id"]
    ),
    "uq_users_username": ConstraintInfo(
        ConstraintType.UNIQUE,
        "users",
        ["username"]
    ),
    "pk_sleep_goals_user_id": ConstraintInfo(
        ConstraintType.PRIMARY_KEY,
        "sleep_goals",
        ["user_id"]
    ),
    "fk_sleep_goals_user_id": ConstraintInfo(
        ConstraintType.FOREIGN_KEY,
        "sleep_goals",
        ["user_id"]
    ),
    "pk_sleep_notes_id": ConstraintInfo(
        ConstraintType.PRIMARY_KEY,
        "sleep_notes",
        ["id"]
    ),
    "chk_sleep_notes_rating": ConstraintInfo(
        ConstraintType.CHECK,
        "sleep_notes",
        ["rating"]
    ),
    "fk_sleep_notes_user_id": ConstraintInfo(
        ConstraintType.FOREIGN_KEY,
        "sleep_notes",
        ["user_id"]
    ),
    "uq_sleep_notes_user_id_note_date": ConstraintInfo(
        ConstraintType.UNIQUE,
        "sleep_notes",
        ["user_id", "note_date"]
    )
}
