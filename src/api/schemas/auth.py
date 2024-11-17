from src.api.schemas.base import BaseSchema


class LoginData(BaseSchema):
    username: str
    password: str


class Tokens(BaseSchema):
    access_token: str
    refresh_token: str


class CreatedTokens(Tokens):
    refresh_token_id: str
