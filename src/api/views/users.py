from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.actions.users import get_user_by_id, create_new_user, delete_user_by_id, update_user_by_id
from src.api.schemas.users import UserReadResponse, UserCreateRequest, UserUpdateRequest
from src.api.utils.tokens import decode_access_token
from src.api.views import http_bearer, user_not_found, database_conflict, no_parameters
from src.core.session import get_session

users_router = APIRouter(prefix='/users', tags=["Users"])


@users_router.get("/", response_model=UserReadResponse, status_code=status.HTTP_200_OK)
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                   session: AsyncSession = Depends(get_session)
                   ) -> UserReadResponse:
    token = credentials.credentials
    payload = decode_access_token(token)
    user = await get_user_by_id(payload.sub, session)
    if user is None:
        raise user_not_found

    return UserReadResponse.model_validate(user)


@users_router.post("/")
async def create_user(body: UserCreateRequest,
                      session: AsyncSession = Depends(get_session)
                      ) -> Response:
    try:
        await create_new_user(body, session)
    except IntegrityError:
        raise database_conflict

    return Response(status_code=status.HTTP_201_CREATED)


@users_router.delete("/")
async def delete_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                      session: AsyncSession = Depends(get_session)
                      ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    deleted = await delete_user_by_id(payload.sub, session)
    if not deleted:
        raise user_not_found

    return Response(status_code=status.HTTP_200_OK)


@users_router.patch("/")
async def update_user(body: UserUpdateRequest,
                      credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                      session: AsyncSession = Depends(get_session)
                      ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    updated_user_params = body.model_dump(exclude_none=True)
    if not updated_user_params:
        raise no_parameters
    try:
        updated = await update_user_by_id(payload.sub, updated_user_params, session)
        if not updated:
            raise user_not_found
    except IntegrityError:
        raise database_conflict

    return Response(status_code=status.HTTP_200_OK)
