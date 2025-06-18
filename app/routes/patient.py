from fastapi import APIRouter, Depends, HTTPException
from fhir.resources.patient import Patient
from app.services.fhir_service import FHIRService
from aiobreaker import CircuitBreakerError

router = APIRouter()

def get_fhir_service():
    return FHIRService()

def remove_extra_fields(data: dict) -> dict:
    # Remove non-standard fields like meta.createdAt
    if "meta" in data and isinstance(data["meta"], dict):
        data["meta"].pop("createdAt", None)
    return data

@router.post("/patients", response_model=Patient)
async def create_patient(
    patient: Patient,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    try:
        # Use mode="json" to ensure all fields are serializable
        result = await fhir_service.create_patient(patient.model_dump(mode="json"))
        result = remove_extra_fields(result)
        return Patient.model_validate(result)
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable due to repeated backend failures (circuit breaker open)."
        )

@router.get("/patients/{patient_id}", response_model=Patient)
async def get_patient(
    patient_id: str,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    try:
        result = await fhir_service.fetch_patient_by_id(patient_id)
        result = remove_extra_fields(result)
        return Patient.model_validate(result)
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable due to repeated backend failures (circuit breaker open)."
        )

@router.put("/patients/{patient_id}", response_model=Patient)
async def update_patient(
    patient_id: str,
    patient: Patient,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    try:
        result = await fhir_service.update_patient(patient_id, patient.model_dump(mode="json"))
        result = remove_extra_fields(result)
        return Patient.model_validate(result)
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable due to repeated backend failures (circuit breaker open)."
        )

@router.delete("/patients/{patient_id}")
async def delete_patient(
    patient_id: str,
    fhir_service: FHIRService = Depends(get_fhir_service)
):
    try:
        return await fhir_service.delete_patient(patient_id)
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable due to repeated backend failures (circuit breaker open)."
        )