from pydantic import Field

from src.api.schemas.base import BaseSchema


class LoginData(BaseSchema):
    username: str = Field(..., max_length=50)
    password: str = Field(..., max_length=50)


class Tokens(BaseSchema):
    access_token: str
    refresh_token: str


class CreatedTokens(Tokens):
    refresh_token_id: str


class RefreshTokenPayload(BaseSchema):
    sub: int
    exp: int
    iat: int
    jti: str
    type: str


class AccessTokenPayload(BaseSchema):
    sub: int
    username: str
    exp: int
    iat: int
    type: str
