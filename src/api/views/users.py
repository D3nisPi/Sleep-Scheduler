from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
)

from src.api.actions.users import get_user_by_id, create_new_user, delete_user_by_id, update_user_by_id
from src.api.schemas.users import UserReadResponse, UserCreateRequest, UserUpdateRequest
from src.api.utils.tokens import decode_access_token
from src.api.views import (
    http_bearer,
    user_not_found,
    no_parameters,
    no_database_connection_info,
    database_conflict_info,
    bad_request_info,
    user_not_found_info,
    no_body_successful_201_info,
    no_body_successful_200_info,
    unauthorized_info,
    forbidden_info
)
from src.core.session import get_session

users_router = APIRouter(prefix='/users', tags=["Users"])

successful_user_read_info = {"model": UserReadResponse, "description": "Successful Response"}

get_user_responses = {
    HTTP_200_OK: successful_user_read_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: user_not_found_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

create_user_responses = {
    HTTP_201_CREATED: no_body_successful_201_info,
    HTTP_409_CONFLICT: database_conflict_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

delete_user_responses = {
    HTTP_200_OK: no_body_successful_200_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: user_not_found_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

update_user_responses = {
    HTTP_200_OK: no_body_successful_200_info,
    HTTP_400_BAD_REQUEST: bad_request_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: user_not_found_info,
    HTTP_409_CONFLICT: database_conflict_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}


@users_router.get("/", status_code=HTTP_200_OK, response_model=UserReadResponse, responses=get_user_responses)
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
    updated_user_params = body.model_dump(exclude_unset=True)
    if not updated_user_params:
        raise no_parameters

    updated = await update_user_by_id(payload.sub, updated_user_params, session)
    if not updated:
        raise user_not_found

    return Response(status_code=HTTP_200_OK)
