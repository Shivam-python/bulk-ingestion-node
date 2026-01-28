# app/services/bulk_service.py
import asyncio
import logging
import uuid
import time
from app.clients.hospital_client import HospitalClient
from app.core.state import BATCH_STORE

logger = logging.getLogger(__name__)


class BulkService:
    def __init__(self):
        self.client = HospitalClient()
        self.semaphore = asyncio.Semaphore(5)

    async def process_bulk(self, hospitals: list):
        batch_id = str(uuid.uuid4())
        start = time.monotonic()

        BATCH_STORE[batch_id] = {
            "total": len(hospitals),
            "processed_count": 0,
            "failed_count": 0,
            "failed_rows": [],
            "hospitals": [],
            "activated": False,
            "start": start,
        }

        async def worker(row_num, hospital):
            async with self.semaphore:
                try:
                    data = {
                        **hospital,
                        "creation_batch_id": batch_id,
                    }
                    res = await self.client.create_hospital(data)

                    BATCH_STORE[batch_id]["hospitals"].append({
                        "row": row_num,
                        "hospital_id": res["id"],
                        "name": hospital["name"],
                        "status": "created"
                    })
                    BATCH_STORE[batch_id]["processed_count"] += 1
                except Exception as e:
                    logger.error(f"EXCEPTION WHILE CREATING HOSPITAL : {str(e)}")
                    BATCH_STORE[batch_id]["failed_count"] += 1

                    BATCH_STORE[batch_id]["failed_rows"].append({
                        **hospital,
                        "creation_batch_id": batch_id,
                    })

        await asyncio.gather(
            *[worker(i + 1, h) for i, h in enumerate(hospitals)]
        )

        if BATCH_STORE[batch_id]["failed_count"] == 0:
            await self.client.activate_batch(batch_id)
            BATCH_STORE[batch_id]["activated"] = True

        BATCH_STORE[batch_id]["time"] = round(time.monotonic() - start, 2)
        return batch_id

    async def process_bulk_with_id(self, batch_id: str, hospitals: list):
        BATCH_STORE[batch_id].update({
            "status": "processing",
            "failed_rows": [],
            "hospitals": []
        })

        await self.process_hospitals(batch_id, hospitals)

        if BATCH_STORE[batch_id]["failed"] == 0:
            await self.client.activate_batch(batch_id)
            BATCH_STORE[batch_id]["activated"] = True
            BATCH_STORE[batch_id]["status"] = "completed"
        else:
            BATCH_STORE[batch_id]["status"] = "failed"

    async def process_hospitals(self, batch_id: str, hospitals: list):
        async def worker(row_num, hospital):
            async with self.semaphore:
                try:
                    data = {**hospital, "creation_batch_id": batch_id}
                    res = await self.client.create_hospital(data)

                    BATCH_STORE[batch_id]["hospitals"].append({
                        "row": row_num,
                        "hospital_id": res["id"],
                        "name": hospital["name"],
                        "status": "created"
                    })
                    BATCH_STORE[batch_id]["processed"] += 1

                except Exception as e:
                    BATCH_STORE[batch_id]["failed"] += 1
                    BATCH_STORE[batch_id]["failed_rows"].append({
                        "row": row_num,
                        "hospital": hospital,
                        "error": str(e)
                    })

        await asyncio.gather(*[worker(i + 1, h) for i, h in enumerate(hospitals)])
