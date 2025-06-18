import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, patch
from fhir.resources.patient import Patient

client = TestClient(app)

@pytest.fixture
def patient_example():
    return {
        "resourceType": "Patient",
        "name": [{"family": "Doe", "given": ["John"]}],
        "gender": "male"
    }

def test_create_patient(patient_example):
    with patch("app.services.fhir_service.FHIRService.create_patient", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = {**patient_example, "id": "123"}
        response = client.post("/patients", json=patient_example)
        assert response.status_code == 200
        assert response.json()["id"] == "123"

def test_get_patient(patient_example):
    with patch("app.services.fhir_service.FHIRService.fetch_patient_by_id", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {**patient_example, "id": "123"}
        response = client.get("/patients/123")
        assert response.status_code == 200
        assert response.json()["id"] == "123"

def test_update_patient(patient_example):
    with patch("app.services.fhir_service.FHIRService.update_patient", new_callable=AsyncMock) as mock_update:
        mock_update.return_value = {**patient_example, "id": "123", "gender": "female"}
        patient_example["gender"] = "female"
        response = client.put("/patients/123", json=patient_example)
        assert response.status_code == 200
        assert response.json()["gender"] == "female"

def test_delete_patient():
    with patch("app.services.fhir_service.FHIRService.delete_patient", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = {"detail": "Patient deleted"}
        response = client.delete("/patients/123")
        assert response.status_code == 200
        assert response.json()["detail"] == "Patient deleted"
