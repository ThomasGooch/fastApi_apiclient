import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def patient_example():
    return {
        "resourceType": "Patient",
        "name": [{"family": "Doe", "given": ["John"]}],
        "gender": "male",
        "birthDate": "1980-01-01",
        "address": [{
            "line": ["123 Main St"],
            "city": "Anytown",
            "state": "CA",
            "postalCode": "12345"
        }]
    }

def test_create_patient(patient_example):
    with patch("app.services.fhir_service.FHIRService.create_patient", return_value=patient_example):
        response = client.post("/patients", json=patient_example)
        assert response.status_code == 200
        assert response.json()["resourceType"] == "Patient"
        assert response.json()["name"][0]["family"] == "Doe"

def test_get_patient(patient_example):
    with patch("app.services.fhir_service.FHIRService.fetch_patient_by_id", return_value=patient_example):
        response = client.get("/patients/123")
        assert response.status_code == 200
        assert response.json()["resourceType"] == "Patient"
        assert response.json()["name"][0]["family"] == "Doe"

def test_update_patient(patient_example):
    updated = dict(patient_example)
    updated["gender"] = "female"
    with patch("app.services.fhir_service.FHIRService.update_patient", return_value=updated):
        response = client.put("/patients/123", json=updated)
        assert response.status_code == 200
        assert response.json()["gender"] == "female"

def test_delete_patient():
    with patch("app.services.fhir_service.FHIRService.delete_patient", return_value={"detail": "Patient deleted"}):
        response = client.delete("/patients/123")
        assert response.status_code == 200
        assert response.json()["detail"] == "Patient deleted"
