from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.auth import authenticate_user_by_password, get_tokens_for_user
from src.api.actions.users import update_user_refresh_token_by_id
from src.api.schemas.auth import TokensResponse, TokensInfo
from src.api.schemas.users import UserSchema
from src.core.session import get_session

auth_router = APIRouter(prefix='/auth', tags=["Auth"])


@auth_router.post("/login/", response_model=TokensResponse, status_code=201)
async def login(user: UserSchema = Depends(authenticate_user_by_password),
                token_info: TokensInfo = Depends(get_tokens_for_user),
                session: AsyncSession = Depends(get_session)
                ) -> TokensResponse:
    await update_user_refresh_token_by_id(user.id, token_info.refresh_jti, session)
    return TokensResponse(
        access_token=token_info.access_token,
        refresh_token=token_info.refresh_token
    )
