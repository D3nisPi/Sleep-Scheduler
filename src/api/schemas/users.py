from src.api.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id: int
    username: str
    display_name: str
    password_hash: str
    refresh_token_id: str | None


class UserReadResponse(BaseSchema):
    id: int
    username: str
    display_name: str

