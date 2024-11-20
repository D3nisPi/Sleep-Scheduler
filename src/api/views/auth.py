from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN
)

from src.api.actions.auth import authenticate_user_by_password, create_tokens, authenticate_user_by_refresh_token
from src.api.actions.users import update_user_refresh_token_by_id
from src.api.schemas.auth import Tokens, LoginData
from src.api.views import (
    http_bearer,
    bad_request_info,
    no_database_connection_info,
    unauthorized_info,
    user_not_found_info,
    forbidden_info
)
from src.core.session import get_session

auth_router = APIRouter(prefix='/auth', tags=["Auth"])

successful_login_info = {"model": Tokens, "description": "Successful Response"}
successful_refresh_info = {"model": Tokens, "description": "Successful Response"}

login_responses = {
    HTTP_201_CREATED: successful_login_info,
    HTTP_400_BAD_REQUEST: bad_request_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_404_NOT_FOUND: user_not_found_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

refresh_responses = {
    HTTP_201_CREATED: successful_refresh_info,
    HTTP_400_BAD_REQUEST: bad_request_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: user_not_found_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}


@auth_router.post("/login/", response_model=Tokens, status_code=HTTP_201_CREATED, responses=login_responses)
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


@auth_router.post("/refresh/", response_model=Tokens, status_code=HTTP_201_CREATED, responses=refresh_responses)
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
