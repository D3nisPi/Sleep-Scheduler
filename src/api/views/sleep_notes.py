from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_201_CREATED,
    HTTP_409_CONFLICT,
    HTTP_403_FORBIDDEN
)

from src.api.actions.sleep_notes import (
    get_sleep_note_by_id_and_user_id,
    get_sleep_note_by_date_and_user_id,
    create_new_sleep_note,
    delete_sleep_note_by_id_and_user_id,
    delete_sleep_note_by_date_and_user_id,
    update_sleep_note_by_id_and_user_id,
    update_sleep_note_by_date_and_user_id
)
from src.api.schemas.errors import CommonErrorResponse
from src.api.schemas.sleep_notes import SleepNoteReadResponse, SleepNoteCreateRequest, SleepNoteUpdateRequest
from src.api.utils.tokens import decode_access_token
from src.api.views import (
    http_bearer,
    bad_request_info,
    unauthorized_info,
    sleep_note_not_found,
    no_database_connection_info,
    no_body_successful_201_info,
    database_conflict_info,
    no_body_successful_200_info,
    no_parameters,
    forbidden_info
)
from src.core.session import get_session

sleep_notes_router = APIRouter(prefix='/notes', tags=["Sleep Notes"])

successful_sleep_note_read_info = {"model": SleepNoteReadResponse, "description": "Successful Response"}
sleep_note_not_found_info = {"model": CommonErrorResponse, "description": "Sleep note not found"}

get_sleep_goal_responses = {
    HTTP_200_OK: successful_sleep_note_read_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: sleep_note_not_found_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

create_sleep_goal_responses = {
    HTTP_201_CREATED: no_body_successful_201_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_409_CONFLICT: database_conflict_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

delete_sleep_note_responses = {
    HTTP_200_OK: no_body_successful_200_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: sleep_note_not_found_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}

update_sleep_note_responses = {
    HTTP_200_OK: no_body_successful_200_info,
    HTTP_400_BAD_REQUEST: bad_request_info,
    HTTP_401_UNAUTHORIZED: unauthorized_info,
    HTTP_403_FORBIDDEN: forbidden_info,
    HTTP_404_NOT_FOUND: sleep_note_not_found_info,
    HTTP_409_CONFLICT: database_conflict_info,
    HTTP_503_SERVICE_UNAVAILABLE: no_database_connection_info
}


@sleep_notes_router.get("/{note_id}", status_code=HTTP_200_OK,
                        response_model=SleepNoteReadResponse, responses=get_sleep_goal_responses)
async def get_sleep_note_by_id(note_id: int,
                               credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                               session: AsyncSession = Depends(get_session)
                               ) -> SleepNoteReadResponse:
    token = credentials.credentials
    payload = decode_access_token(token)
    sleep_note = await get_sleep_note_by_id_and_user_id(note_id, payload.sub, session)
    if sleep_note is None:
        raise sleep_note_not_found

    return SleepNoteReadResponse.model_validate(sleep_note)


@sleep_notes_router.get("/", status_code=HTTP_200_OK,
                        response_model=SleepNoteReadResponse, responses=get_sleep_goal_responses)
async def get_sleep_note_by_date(note_date: date = Query(...),
                                 credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                                 session: AsyncSession = Depends(get_session)
                                 ) -> SleepNoteReadResponse:
    token = credentials.credentials
    payload = decode_access_token(token)
    sleep_note = await get_sleep_note_by_date_and_user_id(note_date, payload.sub, session)
    if sleep_note is None:
        raise sleep_note_not_found

    return SleepNoteReadResponse.model_validate(sleep_note)


@sleep_notes_router.post("/", status_code=HTTP_201_CREATED,
                         response_class=Response, responses=create_sleep_goal_responses)
async def create_sleep_note(body: SleepNoteCreateRequest,
                            credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                            session: AsyncSession = Depends(get_session)
                            ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    await create_new_sleep_note(payload.sub, body, session)
    return Response(status_code=HTTP_201_CREATED)


@sleep_notes_router.delete("/{note_id}", status_code=HTTP_200_OK,
                           response_class=Response, responses=delete_sleep_note_responses)
async def delete_sleep_note_by_id(note_id: int,
                                  credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                                  session: AsyncSession = Depends(get_session)
                                  ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    deleted = await delete_sleep_note_by_id_and_user_id(note_id, payload.sub, session)
    if not deleted:
        raise sleep_note_not_found

    return Response(status_code=HTTP_200_OK)


@sleep_notes_router.delete("/", status_code=HTTP_200_OK,
                           response_class=Response, responses=delete_sleep_note_responses)
async def delete_sleep_note_by_date(note_date: date = Query(...),
                                    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                                    session: AsyncSession = Depends(get_session)
                                    ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    deleted = await delete_sleep_note_by_date_and_user_id(note_date, payload.sub, session)
    if not deleted:
        raise sleep_note_not_found

    return Response(status_code=HTTP_200_OK)


@sleep_notes_router.patch("/{note_id}", status_code=HTTP_200_OK,
                          response_class=Response, responses=update_sleep_note_responses)
async def update_sleep_note_by_id(note_id: int,
                                  body: SleepNoteUpdateRequest,
                                  credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                                  session: AsyncSession = Depends(get_session)
                                  ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    updated_sleep_goal_params = body.model_dump(exclude_unset=True)
    if not updated_sleep_goal_params:
        raise no_parameters

    updated = await update_sleep_note_by_id_and_user_id(note_id, payload.sub, updated_sleep_goal_params, session)
    if not updated:
        raise sleep_note_not_found

    return Response(status_code=HTTP_200_OK)


@sleep_notes_router.patch("/", status_code=HTTP_200_OK,
                          response_class=Response, responses=update_sleep_note_responses)
async def update_sleep_note_by_date(body: SleepNoteUpdateRequest,
                                    note_date: date = Query(...),
                                    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
                                    session: AsyncSession = Depends(get_session)
                                    ) -> Response:
    token = credentials.credentials
    payload = decode_access_token(token)
    updated_sleep_goal_params = body.model_dump(exclude_unset=True)
    if not updated_sleep_goal_params:
        raise no_parameters

    updated = await update_sleep_note_by_date_and_user_id(note_date, payload.sub, updated_sleep_goal_params, session)
    if not updated:
        raise sleep_note_not_found

    return Response(status_code=HTTP_200_OK)
