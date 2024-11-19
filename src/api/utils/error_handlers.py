from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.schemas.errors import DatabaseErrorResponse, DatabaseErrorDetail
from src.api.utils.constraints import constraints


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(IntegrityError)
    def handle_database_error(request: Request, e: IntegrityError) -> JSONResponse:
        error_message = str(e.orig)
        errors = []

        for constraint_name, constraint_info in constraints.items():
            if constraint_name in error_message:
                errors.append(
                    DatabaseErrorDetail(
                        error_type=constraint_info.type.value,
                        table=constraint_info.table,
                        fields=constraint_info.fields,
                    )
                )

        if not errors:
            errors.append(
                DatabaseErrorDetail(
                    error_type="unknown",
                    table="unknown",
                    fields=["unknown"],
                )
            )

        response = DatabaseErrorResponse(detail=errors)
        return JSONResponse(
            content=response.model_dump(),
            status_code=status.HTTP_409_CONFLICT
        )
