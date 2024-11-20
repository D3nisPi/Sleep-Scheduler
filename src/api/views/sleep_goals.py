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

from src.api.actions.sleep_goals import (
    get_sleep_goal_by_user_id,
    create_new_sleep_goal,
    delete_sleep_goal_by_id,
    update_sleep_goal_by_id
)
from src.api.schemas.errors import CommonErrorResponse
from src.api.schemas.sleep_goals import SleepGoalReadResponse, SleepGoalCreateRequest, SleepGoalUpdateRequest
from src.api.utils.tokens import decode_access_token
from src.api.views import (
    http_bearer,
    no_parameters,
    sleep_goal_not_found,
    no_database_connection_info,
    database_conflict_info,
    no_body_successful_200_info,
    no_body_successful_201_info,
    bad_request_info,
    unauthorized_info,
    forbidden_info
)
from src.core.session import get_session

sleep_goals_router = APIRouter(prefix='/goals', tags=["Sleep Goals"])

successful_sleep_goal_read_info = {"model": SleepGoalReadResponse, "description": "Successful Response"}
sleep_goal_not_found_info = {"model": CommonErrorResponse, "description": "Sleep goal not found"}

get_sleep_goal_responses = {
    HTTP_200_OK: successful_sleep_goal_read_info,
    HTTP_400_BAD_REQUEST: bad_request_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: sleep_goal_not_found_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

create_sleep_goal_responses = {
    HTTP_201_CREATED: no_body_successful_201_info,
    HTTP_400_BAD_REQUEST: bad_request_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_409_CONFLICT: database_conflict_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

delete_sleep_goal_responses = {
    HTTP_200_OK: no_body_successful_200_info,
    HTTP_400_BAD_REQUEST: bad_request_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: sleep_goal_not_found_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

update_sleep_goal_responses = {
    HTTP_200_OK: no_body_successful_200_info,
    HTTP_400_BAD_REQUEST: bad_request_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: sleep_goal_not_found_info,
    HTTP_409_CONFLICT: database_conflict_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}


@sleep_goals_router.get("/", status_code=HTTP_200_OK,
                        response_model=SleepGoalReadResponse, responses=get_sleep_goal_responses)
async def get_sleep_goal(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                         session: AsyncSession = Depends(get_session)
                         ) -> SleepGoalReadResponse:
    token = credentials.credentials
    payload = decode_access_token(token)
    sleep_goal = await get_sleep_goal_by_user_id(payload.sub, session)
    if sleep_goal is None:
        raise sleep_goal_not_found

    return SleepGoalReadResponse.model_validate(sleep_goal)


@sleep_goals_router.post("/", status_code=HTTP_201_CREATED,
                         response_class=Response, responses=create_sleep_goal_responses)
async def create_sleep_goal(body: SleepGoalCreateRequest,
                            credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                            session: AsyncSession = Depends(get_session)
                            ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    await create_new_sleep_goal(payload.sub, body, session)
    return Response(status_code=HTTP_201_CREATED)


@sleep_goals_router.delete("/", status_code=HTTP_200_OK,
                           response_class=Response, responses=delete_sleep_goal_responses)
async def delete_sleep_goal(credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                            session: AsyncSession = Depends(get_session)
                            ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    deleted = await delete_sleep_goal_by_id(payload.sub, session)
    if not deleted:
        raise sleep_goal_not_found

    return Response(status_code=HTTP_200_OK)


@sleep_goals_router.patch("/", status_code=HTTP_200_OK,
                          response_class=Response, responses=update_sleep_goal_responses)
async def update_sleep_goal(body: SleepGoalUpdateRequest,
                            credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                            session: AsyncSession = Depends(get_session)
                            ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    updated_sleep_goal_params = body.model_dump(exclude_unset=True)
    if not updated_sleep_goal_params:
        raise no_parameters

    updated = await update_sleep_goal_by_id(payload.sub, updated_sleep_goal_params, session)
    if not updated:
        raise sleep_goal_not_found

    return Response(status_code=HTTP_200_OK)
