# app/clients/hospital_client.py
import httpx
from typing import Dict

BASE_URL = "https://hospital-directory.onrender.com"


class HospitalClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10)

    async def create_hospital(self, payload: Dict):
        r = await self.client.post(f"{BASE_URL}/hospitals/", json=payload)
        r.raise_for_status()
        return r.json()

    async def activate_batch(self, batch_id: str):
        r = await self.client.patch(f"{BASE_URL}/hospitals/batch/{batch_id}/activate")
        r.raise_for_status()
        return r.json()
