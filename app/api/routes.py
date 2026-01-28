import asyncio
import uuid

from fastapi import APIRouter, UploadFile, File, BackgroundTasks

from app.core.custom_exceptions import FileTypeNotAllowed, AppException
from app.services.background_tasks import run_bulk_process
from app.services.bulk_service import BulkService
from app.utils.csv_parser import parse_csv
from app.core.state import BATCH_STORE
from app.utils.csv_validator import validate_csv
from app.core.response import ResponseBuilder
from app.utils.file_utils import read_limited_file, FileTooLargeError

router = APIRouter()
service = BulkService()


@router.post("/hospitals/bulk")
async def bulk_upload(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise FileTypeNotAllowed()

    content = await read_limited_file(file)
    hospitals = parse_csv(content)

    batch_id = str(uuid.uuid4())

    # Initialize batch as pending
    BATCH_STORE[batch_id] = {
        "status": "processing",
        "total": len(hospitals),
        "processed": 0,
        "failed": 0,
        "activated": False,
    }

    asyncio.create_task(run_bulk_process(batch_id, hospitals))

    return ResponseBuilder.success_response(
        message="Bulk processing started",
        data={"batch_id": batch_id},
        status_code=202
    )


@router.get("/hospitals/bulk/{batch_id}")
def get_status(batch_id: str):
    batch = BATCH_STORE.get(batch_id)

    if not batch:
        return ResponseBuilder.error_response(
            message="Batch ID not found",
            errors=[f"No batch exists with id {batch_id}"],
            status_code=404
        )

    return ResponseBuilder.success_response(
        message="Batch status fetched successfully",
        data=batch
    )


@router.post("/hospitals/bulk/validate")
async def validate_bulk_csv(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise FileTypeNotAllowed()

    content = await read_limited_file(file)
    result = validate_csv(content)

    if result["valid"]:
        return ResponseBuilder.success_response(
            message="CSV validated successfully",
            data=result,
        )
    else:
        return ResponseBuilder.error_response(
            message="CSV validation failed",
            errors=result["errors"],
            status_code=422,
        )


@router.post("/hospitals/bulk/{batch_id}/retry")
async def retry_failed(batch_id: str):
    batch = BATCH_STORE.get(batch_id)
    if not batch:
        raise AppException("Batch not found", 404)

    if not batch["failed_rows"]:
        raise AppException("No failed hospitals to retry", 400)

    hospitals_to_retry = [item["hospital"] for item in batch["failed_rows"]]

    batch["failed"] = 0
    batch["failed_rows"] = []

    asyncio.create_task(run_bulk_process(batch_id, hospitals_to_retry))

    return ResponseBuilder.success_response(
        message="Retry started for failed hospitals",
        data={"batch_id": batch_id},
        status_code=202
    )
