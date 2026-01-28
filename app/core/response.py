from datetime import datetime
from typing import Any, List, Dict, Optional
from fastapi.responses import JSONResponse
import uuid


class ResponseBuilder:

    @staticmethod
    def _meta(status_code: int) -> Dict:
        return {
            "status_code": status_code,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": str(uuid.uuid4()),
        }

    @staticmethod
    def success_response(
        message: str = "Request successful",
        data: Optional[Any] = None,
        status_code: int = 200,
    ):
        body = {
            "success": True,
            "message": message,
            "data": data or {},
            "errors": [],
            "meta": ResponseBuilder._meta(status_code),
        }
        return JSONResponse(status_code=status_code, content=body)

    @staticmethod
    def error_response(
        message: str = "Request failed",
        errors: Optional[List[Any]] = None,
        status_code: int = 400,
    ):
        body = {
            "success": False,
            "message": message,
            "data": {},
            "errors": errors or [],
            "meta": ResponseBuilder._meta(status_code),
        }
        return JSONResponse(status_code=status_code, content=body)

    @staticmethod
    def exception_response(exc: Exception):
        return ResponseBuilder.error_response(
            message="Internal server error",
            errors=[str(exc)],
            status_code=500,
        )
