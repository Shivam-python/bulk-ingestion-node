import asyncio
import logging
from app.clients.hospital_client import HospitalClient
from app.key_store.redis_store import set_batch, get_batch, update_batch, add_success, increment_processed, add_failure, \
    increment_failed, set_status, activate_batch, get_batch_summary
from app.monitoring.metrics import (
    ACTIVE_BATCH_JOBS,
    HOSPITALS_PROCESSED,
)

logger = logging.getLogger(__name__)


class BulkService:
    def __init__(self):
        self.client = HospitalClient()

    async def process_bulk_with_id(self, batch_id: str, hospitals: list):
        ACTIVE_BATCH_JOBS.inc()  # 🔥 Batch started

        try:
            set_status(batch_id, "processing")

            await self.process_hospitals(batch_id, hospitals)

            batch = get_batch_summary(batch_id)  # read from Redis hash

            if batch["failed"] == 0:
                await self.client.activate_batch(batch_id)
                set_status(batch_id, "completed")
                activate_batch(batch_id, True)
            else:
                set_status(batch_id, "failed")

        finally:
            ACTIVE_BATCH_JOBS.dec()

    async def process_hospitals(self, batch_id: str, hospitals: list):
        semaphore = asyncio.Semaphore(10)

        async def worker(row_num, hospital):
            async with semaphore:
                try:
                    payload = {**hospital, "creation_batch_id": batch_id}
                    res = await self.client.create_hospital(payload)

                    add_success(batch_id, {
                        "row": row_num,
                        "hospital_id": res["id"],
                        "name": hospital["name"],
                        "status": "created"
                    })

                    increment_processed(batch_id)

                    # ✅ SUCCESS METRIC
                    HOSPITALS_PROCESSED.labels(status="success").inc()

                except Exception as e:
                    add_failure(batch_id, {
                        "row": row_num,
                        "hospital": hospital,
                        "error": str(e)
                    })

                    increment_failed(batch_id)
                    HOSPITALS_PROCESSED.labels(status="failed").inc()

        await asyncio.gather(*[worker(i + 1, h) for i, h in enumerate(hospitals)])
