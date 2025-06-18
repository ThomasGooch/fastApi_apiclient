import os
from fhirclient import client
from fhirclient.models.patient import Patient as FHIRPatient
from fastapi import HTTPException
import requests

FHIR_BACKEND_URL = os.getenv("BACKENDURL", "http://localhost:8080")

settings = {
    'app_id': 'my_web_app',
    'api_base': FHIR_BACKEND_URL,
    'verify_ssl': False  # Set to True in production with valid certs
}

def _clean_meta_created_at(resource: dict) -> dict:
    if "meta" in resource and isinstance(resource["meta"], dict):
        resource["meta"].pop("createdAt", None)
    return resource

class FHIRService:
    def __init__(self):
        self.smart = client.FHIRClient(settings=settings)
        # Set verify=False on the underlying requests.Session for full effect
        if hasattr(self.smart.server, 'session'):
            self.smart.server.session.verify = False

    async def create_patient(self, patient_json: dict):
        patient = FHIRPatient(patient_json)
        created = patient.create(self.smart.server)
        # Handle both dict and FHIRPatient return types
        patient_id = getattr(created, "id", None) if hasattr(created, "id") else created.get("id") if isinstance(created, dict) else None
        if not created or not patient_id:
            raise HTTPException(status_code=500, detail="Failed to create patient")
        data = created.as_json() if hasattr(created, "as_json") else created
        data = _clean_meta_created_at(data)
        return data

    async def fetch_patient_by_id(self, patient_id: str):
        url = f"{self.smart.server.base_uri}Patient/{patient_id}"
        resp = self.smart.server.session.get(url)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Patient not found")
        data = resp.json()
        data = _clean_meta_created_at(data)
        return data

    async def update_patient(self, patient_id: str, patient_json: dict):
        url = f"{self.smart.server.base_uri}Patient/{patient_id}"
        resp = self.smart.server.session.put(url, json=patient_json)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Patient not found")
        data = resp.json()
        data = _clean_meta_created_at(data)
        return data

    async def delete_patient(self, patient_id: str):
        url = f"{self.smart.server.base_uri}Patient/{patient_id}"
        resp = self.smart.server.session.delete(url)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Patient not found")
        if resp.status_code not in (200, 204):
            raise HTTPException(status_code=500, detail="Failed to delete patient")
        return {"detail": "Patient deleted"}
