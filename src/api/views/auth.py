from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.actions.auth import authenticate_user_by_password, create_tokens, authenticate_user_by_refresh_token
from src.api.actions.users import update_user_refresh_token_by_id
from src.api.schemas.auth import Tokens, LoginData
from src.core.session import get_session

auth_router = APIRouter(prefix='/auth', tags=["Auth"])

http_bearer = HTTPBearer()


@auth_router.post("/login/", response_model=Tokens, status_code=status.HTTP_201_CREATED)
async def login(body: LoginData,
                session: AsyncSession = Depends(get_session)
                ) -> Tokens:
    user = await authenticate_user_by_password(body, session)
    tokens_info = create_tokens(user)
    await update_user_refresh_token_by_id(user.id, tokens_info.refresh_token_id, session)
    return Tokens(
        access_token=tokens_info.access_token,
        refresh_token=tokens_info.refresh_token
    )


@auth_router.post("/refresh/", response_model=Tokens, status_code=status.HTTP_201_CREATED)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                        session: AsyncSession = Depends(get_session)
                        ) -> Tokens:
    token = credentials.credentials
    user = await authenticate_user_by_refresh_token(token, session)
    tokens_info = create_tokens(user)
    await update_user_refresh_token_by_id(user.id, tokens_info.refresh_token_id, session)
    return Tokens(
        access_token=tokens_info.access_token,
        refresh_token=tokens_info.refresh_token
    )
