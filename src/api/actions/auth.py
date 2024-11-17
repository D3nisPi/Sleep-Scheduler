import uuid
from datetime import datetime, UTC

import bcrypt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.actions.users import get_user_by_username, get_user_by_id
from src.api.schemas.auth import LoginData, CreatedTokens
from src.api.schemas.users import UserSchema
from src.api.utils.tokens import create_access_token, create_refresh_token, decode_refresh_token


async def authenticate_user_by_password(body: LoginData,
                                        session: AsyncSession
                                        ) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )
    user = await get_user_by_username(body.username, session)
    if user is None:
        raise credentials_exception

    if not bcrypt.checkpw(body.password.encode(), bytes.fromhex(user.password_hash)):
        raise credentials_exception

    return UserSchema.model_validate(user)


async def authenticate_user_by_refresh_token(token: str,
                                             session: AsyncSession
                                             ) -> UserSchema:

    payload = decode_refresh_token(token)

    user = await get_user_by_id(payload.sub, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.refresh_token_id != payload.jti:
        user.refresh_token_id = None
        await session.commit()
        raise HTTPException(status_code=401, detail="Invalid jti")

    return UserSchema.model_validate(user)


def create_tokens(user: UserSchema) -> CreatedTokens:
    now = datetime.now(UTC)
    refresh_token_id = uuid.uuid4().hex

    access_token = create_access_token(user.id, user.username, now)
    refresh_token = create_refresh_token(user.id, refresh_token_id, now)

    created_tokens = CreatedTokens(
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_token_id=refresh_token_id
    )
    return created_tokens
