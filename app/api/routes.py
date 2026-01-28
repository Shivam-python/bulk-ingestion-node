# app/api/routes.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
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
    try:
        if file.content_type != "text/csv":
            return ResponseBuilder.error_response(
                message="Only CSV files are allowed",
                status_code=415
            )

        content = await read_limited_file(file)
        hospitals = parse_csv(content)

        batch_id = await service.process_bulk(hospitals)
        batch_data = BATCH_STORE.get(batch_id)

        return ResponseBuilder.success_response(
            message="Bulk hospital processing completed",
            data=batch_data,
            status_code=201
        )
    except FileTooLargeError as e:
        return ResponseBuilder.error_response(
            message="File too large",
            errors=[str(e)],
            status_code=413
        )
    except ValueError as e:
        return ResponseBuilder.error_response(
            message="Invalid CSV data",
            errors=[str(e)],
            status_code=422
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
    content = (await file.read()).decode()
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
