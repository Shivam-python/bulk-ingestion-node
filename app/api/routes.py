import asyncio
import uuid

from fastapi import APIRouter, UploadFile, File, BackgroundTasks

from app.core.custom_exceptions import FileTypeNotAllowed, AppException, CSVValidationException
from app.queue.tasks import process_bulk_task, retry_bulk_process_task
from app.services.bulk_service import BulkService
from app.utils.csv_parser import parse_csv
from app.core.state import BATCH_STORE
from app.utils.csv_validator import validate_csv
from app.core.response import ResponseBuilder
from app.utils.file_utils import read_limited_file, FileTooLargeError
from app.key_store.redis_store import set_batch, get_batch, update_batch, get_batch_summary, \
    delete_failed_row_data_from_batch, increment_retries

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
    # set_batch(batch_id,{
    #     "status": "processing",
    #     "total": len(hospitals),
    #     "processed": 0,
    #     "failed": 0,
    #     "activated": False,
    # })

    process_bulk_task.delay(batch_id, hospitals)

    return ResponseBuilder.success_response(
        message="Bulk processing started",
        data={"batch_id": batch_id},
        status_code=202
    )


@router.get("/hospitals/bulk/{batch_id}")
def get_status(batch_id: str):
    batch = get_batch_summary(batch_id)

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
    try:
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
    except CSVValidationException as e:
        return ResponseBuilder.error_response(
            message="CSV validation failed",
            errors=[str(e)],
            status_code=422,
        )


@router.post("/hospitals/bulk/{batch_id}/retry")
async def retry_failed(batch_id: str):
    batch = get_batch_summary(batch_id)
    if not batch:
        raise AppException("Batch not found", 404)

    if not batch["failed_rows"]:
        raise AppException("No failed hospitals to retry", 400)

    hospitals_to_retry = [item["hospital"] for item in batch["failed_rows"]]

    update_batch(batch_id, {
        "failed": 0,
        "status": "retrying"
    })

    delete_failed_row_data_from_batch(batch_id)

    increment_retries(batch_id)

    retry_bulk_process_task.delay(batch_id, hospitals_to_retry)

    return ResponseBuilder.success_response(
        message="Retry started for failed hospitals",
        data={"batch_id": batch_id},
        status_code=202
    )
