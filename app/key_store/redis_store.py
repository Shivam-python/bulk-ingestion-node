# app/core/redis_client.py
import redis
import json
from app.config.settings import settings
from typing import Dict, Any

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def set_batch(batch_id: str, data: dict):
    r.set(batch_id, json.dumps(data))


def get_batch(batch_id: str) -> dict:
    data = r.get(batch_id)
    if data:
        return json.loads(data)
    return None


def update_batch(batch_id: str, update_dict: dict):
    batch_key = f"batch:{batch_id}"
    r.hset(batch_key, mapping=update_dict)


def increment_processed(batch_id):
    r.hincrby(f"batch:{batch_id}", "processed", 1)


def increment_failed(batch_id):
    r.hincrby(f"batch:{batch_id}", "failed", 1)


def increment_retries(batch_id):
    batch_key = f"batch:{batch_id}"
    r.hincrby(batch_key, "retries", 1)


def add_success(batch_id, data):
    r.rpush(f"batch:{batch_id}:hospitals", json.dumps(data))


def add_failure(batch_id, data):
    r.rpush(f"batch:{batch_id}:failed_rows", json.dumps(data))


def set_status(batch_id, status):
    r.hset(f"batch:{batch_id}", "status", status)


def activate_batch(batch_id, activated):
    r.hset(f"batch:{batch_id}", "activated", activated)


def get_batch_summary(batch_id: str) -> Dict[str, Any]:
    batch_key = f"batch:{batch_id}"
    hospitals_key = f"{batch_key}:hospitals"
    failed_key = f"{batch_key}:failed_rows"

    if not r.exists(batch_key):
        return None

    # Fetch atomic counters & state
    batch_data = r.hgetall(batch_key)

    # Convert numeric fields
    processed = int(batch_data.get("processed", 0))
    failed = int(batch_data.get("failed", 0))
    activated = batch_data.get("activated", "False") == "True"

    # Fetch lists
    hospitals = [json.loads(x) for x in r.lrange(hospitals_key, 0, -1)]
    failed_rows = [json.loads(x) for x in r.lrange(failed_key, 0, -1)]

    return {
        "batch_id": batch_id,
        "status": batch_data.get("status"),
        "processed": processed,
        "failed": failed,
        "activated": activated,
        "hospitals": hospitals,
        "failed_rows": failed_rows,
    }


def delete_failed_row_data_from_batch(batch_id):
    batch_key = f"batch:{batch_id}"
    failed_key = f"{batch_key}:failed_rows"
    r.delete(failed_key)
