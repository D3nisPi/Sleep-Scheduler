from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.auth import create_tokens, validate_user_by_password
from src.api.actions.users import update_user_refresh_token
from src.api.schemas.auth import TokensResponse, TokensInfo
from src.core.models.users import UsersORM
from src.core.session import get_session

auth = APIRouter(prefix='/auth', tags=["Auth"])


@auth.post("/login/")
async def login(
    user: UsersORM = Depends(validate_user_by_password),
    token_info: TokensInfo = Depends(create_tokens),
    session: AsyncSession = Depends(get_session)
) -> TokensResponse:
    await update_user_refresh_token(user, token_info.refresh_jti, session)
    return TokensResponse(
        access_token=token_info.access_token,
        refresh_token=token_info.refresh_token
    )
