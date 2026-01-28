from fastapi import APIRouter
from app.core.response import ResponseBuilder
import time

router = APIRouter()

START_TIME = time.time()


@router.get("/health")
def health_check():
    uptime = round(time.time() - START_TIME, 2)

    return ResponseBuilder.success_response(
        message="Service is healthy",
        data={
            "status": "ok",
            "uptime_seconds": uptime
        }
    )
