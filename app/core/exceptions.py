from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.response import ResponseBuilder


async def global_exception_handler(request: Request, exc: Exception):
    return ResponseBuilder.exception_response(exc)
