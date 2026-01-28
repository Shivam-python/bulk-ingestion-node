from fastapi import Request
from app.core.response import ResponseBuilder
from app.core.custom_exceptions import AppException


async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, AppException):
        return ResponseBuilder.error_response(
            message=exc.message,
            errors=exc.errors,
            status_code=exc.status_code,
        )

    return ResponseBuilder.error_response(
        message="Internal server error",
        errors=[str(exc)],
        status_code=500,
    )
