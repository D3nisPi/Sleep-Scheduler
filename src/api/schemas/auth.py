from src.api.schemas.base import BaseSchema


class LoginRequest(BaseSchema):
    username: str
    password: str


class TokensResponse(BaseSchema):
    access_token: str
    refresh_token: str


class TokensInfo(TokensResponse):
    refresh_jti: str
