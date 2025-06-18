import os
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from aiobreaker import CircuitBreaker
from fastapi import HTTPException

FHIR_BACKEND_URL = os.getenv("BACKENDURL")

breaker = CircuitBreaker(fail_max=5, timeout_duration=30)

class FHIRService:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=FHIR_BACKEND_URL, verify=False)

    @breaker
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True,
    )
    async def create_patient(self, patient_json: dict):
        try:
            resp = await self.client.post("fhir/Patient", json=patient_json)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=str(e))

    @breaker
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True,
    )
    async def fetch_patient_by_id(self, patient_id: str):
        try:
            resp = await self.client.get(f"fhir/Patient/{patient_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=str(e))

    @breaker
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True,
    )
    async def update_patient(self, patient_id: str, patient_json: dict):
        try:
            resp = await self.client.put(f"fhir/Patient/{patient_id}", json=patient_json)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=str(e))

    @breaker
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True,
    )
    async def delete_patient(self, patient_id: str):
        try:
            resp = await self.client.delete(f"fhir/Patient/{patient_id}")
            resp.raise_for_status()
            return {"detail": "Patient deleted"}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=resp.status_code, detail=str(e))
