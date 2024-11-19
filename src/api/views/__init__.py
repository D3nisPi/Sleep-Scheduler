from fastapi import HTTPException
from fastapi.security import HTTPBearer
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST
)

http_bearer = HTTPBearer()

user_not_found = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail=f"User not found"
)
no_parameters = HTTPException(
    status_code=HTTP_400_BAD_REQUEST,
    detail="At least one specified parameter for user update should be provided",
)
