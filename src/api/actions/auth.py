import uuid
from datetime import datetime, timedelta, UTC

import bcrypt
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.users import get_user_by_username
from src.api.schemas.auth import LoginRequest, TokensInfo
from src.core.config import settings
from src.core.models.users import UsersORM

import jwt

from src.core.session import get_session


async def validate_user_by_password(body: LoginRequest,
                                    session: AsyncSession = Depends(get_session)
                                    ) -> UsersORM:
    user = await authenticate_user_by_password(body.username, body.password, session)
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    return user


async def authenticate_user_by_password(username: str,
                                        password: str,
                                        session: AsyncSession
                                        ) -> UsersORM | None:
    user = await get_user_by_username(username, session)
    if user is None:
        return

    if not bcrypt.checkpw(password.encode(), bytes.fromhex(user.password_hash)):
        return

    return user


def create_tokens(user: UsersORM) -> TokensInfo:
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
