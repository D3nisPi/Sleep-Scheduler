from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_503_SERVICE_UNAVAILABLE
)

from src.api.actions.users import get_user_by_id, create_new_user, delete_user_by_id, update_user_by_id
from src.api.schemas.errors import DatabaseErrorResponse, CommonErrorResponse
from src.api.schemas.users import UserReadResponse, UserCreateRequest, UserUpdateRequest
from src.api.utils.tokens import decode_access_token
from src.api.views import http_bearer, user_not_found, no_parameters
from src.core.session import get_session

users_router = APIRouter(prefix='/users', tags=["Users"])

get_user_responses = {
    HTTP_200_OK: {"model": UserReadResponse, "description": "Successful Response"},
    HTTP_404_NOT_FOUND: {"model": CommonErrorResponse, "description": "User not found"},
    HTTP_503_SERVICE_UNAVAILABLE: {"model": CommonErrorResponse, "description": "Database connection problems"}
}

create_user_responses = {
    HTTP_201_CREATED: {"description": "Successful Response"},
    HTTP_409_CONFLICT: {"model": DatabaseErrorResponse, "description": "Database conflict"},
    HTTP_503_SERVICE_UNAVAILABLE: {"model": CommonErrorResponse, "description": "Database connection problems"}
}

delete_user_responses = {
    HTTP_200_OK: {"description": "Successful Response"},
    HTTP_404_NOT_FOUND: {"model": CommonErrorResponse, "description": "User not found"},
    HTTP_503_SERVICE_UNAVAILABLE: {"model": CommonErrorResponse, "description": "Database connection problems"}
}

update_user_responses = {
    HTTP_200_OK: {"description": "Successful Response"},
    HTTP_400_BAD_REQUEST: {"model": CommonErrorResponse, "description": "No parameters to update were given"},
    HTTP_404_NOT_FOUND: {"model": CommonErrorResponse, "description": "User not found"},
    HTTP_409_CONFLICT: {"model": DatabaseErrorResponse, "description": "Database conflict"},
    HTTP_503_SERVICE_UNAVAILABLE: {"model": CommonErrorResponse, "description": "Database connection problems"}
}


@users_router.get("/", status_code=HTTP_200_OK, responses=get_user_responses)
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                   session: AsyncSession = Depends(get_session)
                   ) -> UserReadResponse:
    token = credentials.credentials
    payload = decode_access_token(token)
    user = await get_user_by_id(payload.sub, session)
    if user is None:
        raise user_not_found

    return UserReadResponse.model_validate(user)


@users_router.post("/", status_code=HTTP_201_CREATED, response_class=Response, responses=create_user_responses)
async def create_user(body: UserCreateRequest,
                      session: AsyncSession = Depends(get_session)
                      ) -> Response:
    await create_new_user(body, session)
    return Response(status_code=HTTP_201_CREATED)


@users_router.delete("/", status_code=HTTP_200_OK, response_class=Response, responses=delete_user_responses)
async def delete_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                      session: AsyncSession = Depends(get_session)
                      ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    deleted = await delete_user_by_id(payload.sub, session)
    if not deleted:
        raise user_not_found

    return Response(status_code=HTTP_200_OK)


@users_router.patch("/", status_code=HTTP_200_OK, response_class=Response, responses=update_user_responses)
async def update_user(body: UserUpdateRequest,
                      credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                      session: AsyncSession = Depends(get_session)
                      ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    updated_user_params = body.model_dump(exclude_none=True)
    if not updated_user_params:
        raise no_parameters

    updated = await update_user_by_id(payload.sub, updated_user_params, session)
    if not updated:
        raise user_not_found

    return Response(status_code=HTTP_200_OK)
