import asyncio
from app.queue.celery_app import celery_app
from app.services.background_tasks import run_bulk_process
from app.services.bulk_service import BulkService

service = BulkService()


@celery_app.task(bind=True, max_retries=3)
def process_bulk_task(self, batch_id: str, hospitals: list):
    try:
        asyncio.run(service.process_bulk_with_id(batch_id, hospitals))
    except Exception as e:
        raise self.retry(exc=e, countdown=10)


@celery_app.task(bind=True, max_retries=3)
def retry_bulk_process_task(self, batch_id: str, hospitals: list):
    try:
        asyncio.run(run_bulk_process(batch_id, hospitals))
    except Exception as e:
        raise self.retry(exc=e, countdown=10)
