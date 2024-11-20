from fastapi import HTTPException
from fastapi.security import HTTPBearer
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST
)

from src.api.schemas.errors import CommonErrorResponse, DatabaseErrorResponse

http_bearer = HTTPBearer()

user_not_found = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail=f"User not found"
)
sleep_goal_not_found = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail=f"Sleep goal not found"
)
no_parameters = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="At least one specified parameter for update should be provided",
)

no_body_successful_200_info = {"description": "Successful Response"}
no_body_successful_201_info = {"description": "Successful Response"}
bad_request_info = {"model": CommonErrorResponse, "description": "Bad request"}
user_not_found_info = {"model": CommonErrorResponse, "description": "User not found"}
unauthorized_info = {"model": CommonErrorResponse, "description": "Unauthorized"}
no_database_connection_info = {"model": CommonErrorResponse, "description": "Database connection problems"}
database_conflict_info = {"model": DatabaseErrorResponse, "description": "Database conflict"}
