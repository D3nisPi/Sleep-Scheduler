from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokensInfo(TokensResponse):
    refresh_jti: str
