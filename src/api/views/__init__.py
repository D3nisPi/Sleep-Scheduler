from fastapi import HTTPException
from fastapi.security import HTTPBearer
from starlette import status

http_bearer = HTTPBearer()

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"User not found"
)
database_conflict = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail=f"Database conflict"
)
no_parameters = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="At least one specified parameter for user update should be provided",
)
