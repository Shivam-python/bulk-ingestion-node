import asyncio
from app.services.bulk_service import BulkService
from app.core.logger import get_logger

logger = get_logger()
service = BulkService()


async def run_bulk_process(batch_id: str, hospitals: list):
    try:
        logger.info("Background bulk job started", extra={"batch_id": batch_id})
        await service.process_bulk_with_id(batch_id, hospitals)
        logger.info("Background bulk job finished", extra={"batch_id": batch_id})
    except Exception as e:
        logger.error("Bulk job failed", extra={"batch_id": batch_id, "error": str(e)})
