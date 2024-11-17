from datetime import datetime, timedelta

import jwt
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
