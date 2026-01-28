import httpx
from typing import Dict
from app.config.settings import settings


class HospitalClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10)
        self.BASE_URL = settings.HOSPITAL_API_URL

    async def create_hospital(self, payload: Dict):
        r = await self.client.post(f"{self.BASE_URL}/hospitals/", json=payload)
        r.raise_for_status()
        return r.json()

    async def activate_batch(self, batch_id: str):
        r = await self.client.patch(f"{self.BASE_URL}/hospitals/batch/{batch_id}/activate")
        r.raise_for_status()
        return r.json()
