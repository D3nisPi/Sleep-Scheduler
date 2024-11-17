from pydantic import Field

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


class UserCreateRequest(BaseSchema):
    username: str = Field(..., max_length=50)
    display_name: str = Field(..., max_length=50)
    password: str = Field(..., max_length=50)


class UserUpdateRequest(BaseSchema):
    username: str | None = Field(None, max_length=50)
    display_name: str | None = Field(None, max_length=50)
