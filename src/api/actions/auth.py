import uuid
from datetime import datetime, timedelta, UTC

import bcrypt
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.users import get_user_by_username
from src.api.schemas.auth import LoginRequest, TokensInfo
from src.api.schemas.users import UserSchema
from src.core.config import settings

import jwt

from src.core.session import get_session


async def authenticate_user_by_password(body: LoginRequest,
                                        session: AsyncSession = Depends(get_session)
                                        ) -> UserSchema:
    credentials_exception = HTTPException(status_code=401, detail="Invalid username or password")
    user = await get_user_by_username(body.username, session)
    if user is None:
        raise credentials_exception

    if not bcrypt.checkpw(body.password.encode(), bytes.fromhex(user.password_hash)):
        raise credentials_exception

    return UserSchema.model_validate(user)


def get_tokens_for_user(user: UserSchema = Depends(authenticate_user_by_password)) -> TokensInfo:
    return create_tokens(user)


def create_tokens(user: UserSchema) -> TokensInfo:
    now = datetime.now(UTC)
    jti = uuid.uuid4().hex

    access_token = create_token(get_access_token_payload(user.id, user.username, now))
    refresh_token = create_token(get_refresh_token_payload(user.id, jti, now))

    info = TokensInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_jti=jti
    )
    return info


def get_access_token_payload(user_id, username, iat: datetime):
    return {
        "sub": user_id,
        "username": username,
        "exp": iat + timedelta(minutes=settings.jwt.access_token_expiration_minutes),
        "iat": iat,
        "type": "access"
    }


def get_refresh_token_payload(user_id, jti: str, iat: datetime):
    return {
        "sub": user_id,
        "exp": iat + timedelta(days=settings.jwt.refresh_token_expiration_days),
        "iat": iat,
        "jti": jti,
        "type": "refresh"
    }


def create_token(payload: dict):
    return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
