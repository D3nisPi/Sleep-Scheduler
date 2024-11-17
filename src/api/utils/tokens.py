from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from pydantic import ValidationError
from starlette import status

from src.api.schemas.auth import RefreshTokenPayload, AccessTokenPayload
from src.core.config import settings


def create_access_token(user_id: int,
                        username: str,
                        issued_at: datetime
                        ) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "exp": issued_at + timedelta(minutes=settings.jwt.access_token_expiration_minutes),
        "iat": issued_at,
        "type": "access"
    }
    return jwt.encode(payload, settings.jwt.secret_key, settings.jwt.algorithm)


def create_refresh_token(user_id: int,
                         json_token_id: str,
                         issued_at: datetime
                         ) -> str:
    payload = {
        "sub": user_id,
        "exp": issued_at + timedelta(days=settings.jwt.refresh_token_expiration_days),
        "iat": issued_at,
        "jti": json_token_id,
        "type": "refresh"
    }
    return jwt.encode(payload, settings.jwt.secret_key, settings.jwt.algorithm)


def decode_token(token: str) -> dict:
    invalid_token = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )
    malformed_token = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Malformed token"
    )

    try:
        payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
    except jwt.InvalidSignatureError:
        raise invalid_token
    except jwt.DecodeError:
        raise malformed_token
    except jwt.InvalidTokenError:
        raise invalid_token

    return payload


def decode_access_token(token: str) -> AccessTokenPayload:
    token_data = decode_token(token)
    try:
        payload = AccessTokenPayload(**token_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token data"
        )
    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type. Expected: 'access'"
        )

    return payload


def decode_refresh_token(token: str) -> RefreshTokenPayload:
    token_data = decode_token(token)
    try:
        payload = RefreshTokenPayload(**token_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token data"
        )
    if payload.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type. Expected: 'refresh'"
        )

    return payload
