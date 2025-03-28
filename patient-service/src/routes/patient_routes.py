from fastapi import APIRouter, Depends, Query, Path, Body, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import uuid

from ..database import get_db
from ..controllers.patient_controller import PatientController
from ..controllers.medical_record_controller import MedicalRecordController
from ..utils.response import success_response
from ..utils.jwt_handler import get_current_user_with_roles
from ..models.patient import Patient
from ..models.medical_record import MedicalRecord

# Create router
router = APIRouter(tags=["Patients"])

@router.get("/", response_model=Dict[str, Any])
async def get_patients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search term for patient name or email"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    practitioner_id: Optional[str] = Query(None, description="Filter by practitioner ID"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
    db: Session = Depends(get_db)
):
    """
    Get a list of patients with optional filtering.
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    - **search**: Optional search term for patient name or email
    - **user_id**: Optional filter by user ID
    - **practitioner_id**: Optional filter by practitioner ID
    """
    patients = await PatientController.get_patients(
        skip=skip,
        limit=limit,
        search=search,
        user_id=user_id,
        practitioner_id=practitioner_id,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        data=[{
            "id": str(patient.id),
            "user_id": str(patient.user_id),
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email,
            "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            "gender": patient.gender,
            "phone": patient.phone,
            "address": patient.address,
            "insurance_provider": patient.insurance_provider,
            "insurance_number": patient.insurance_number,
            "created_at": patient.created_at.isoformat() if patient.created_at else None,
            "updated_at": patient.updated_at.isoformat() if patient.updated_at else None
        } for patient in patients],
        message=f"Retrieved {len(patients)} patients"
    )

@router.get("/{patient_id}", response_model=Dict[str, Any])
async def get_patient(
    patient_id: str = Path(..., description="Patient ID"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner", "patient"])),
    db: Session = Depends(get_db)
):
    """
    Get a patient by ID.
    
    - **patient_id**: Patient ID
    """
    patient = await PatientController.get_patient_by_id(
        patient_id=patient_id,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        data={
            "id": str(patient.id),
            "user_id": str(patient.user_id),
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email,
            "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            "gender": patient.gender,
            "phone": patient.phone,
            "address": patient.address,
            "insurance_provider": patient.insurance_provider,
            "insurance_number": patient.insurance_number,
            "created_at": patient.created_at.isoformat() if patient.created_at else None,
            "updated_at": patient.updated_at.isoformat() if patient.updated_at else None
        },
        message="Patient retrieved successfully"
    )

@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: Dict[str, Any] = Body(..., description="Patient data"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
    db: Session = Depends(get_db)
):
    """
    Create a new patient.
    
    - **patient_data**: Patient data
    """
    patient = await PatientController.create_patient(
        patient_data=patient_data,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        data={
            "id": str(patient.id),
            "user_id": str(patient.user_id),
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email
        },
        message="Patient created successfully"
    )

@router.put("/{patient_id}", response_model=Dict[str, Any])
async def update_patient(
    patient_id: str = Path(..., description="Patient ID"),
    patient_data: Dict[str, Any] = Body(..., description="Updated patient data"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner", "patient"])),
    db: Session = Depends(get_db)
):
    """
    Update a patient.
    
    - **patient_id**: Patient ID
    - **patient_data**: Updated patient data
    """
    patient = await PatientController.update_patient(
        patient_id=patient_id,
        patient_data=patient_data,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        data={
            "id": str(patient.id),
            "user_id": str(patient.user_id),
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "email": patient.email,
            "updated_at": patient.updated_at.isoformat() if patient.updated_at else None
        },
        message="Patient updated successfully"
    )

@router.delete("/{patient_id}", response_model=Dict[str, Any])
async def delete_patient(
    patient_id: str = Path(..., description="Patient ID"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin"])),
    db: Session = Depends(get_db)
):
    """
    Delete a patient.
    
    - **patient_id**: Patient ID
    """
    result = await PatientController.delete_patient(
        patient_id=patient_id,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        message=result["message"]
    )

@router.get("/{patient_id}/medical-records", response_model=Dict[str, Any])
async def get_patient_medical_records(
    patient_id: str = Path(..., description="Patient ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    record_type: Optional[str] = Query(None, description="Filter by record type"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner", "patient"])),
    db: Session = Depends(get_db)
):
    """
    Get a list of medical records for a patient.
    
    - **patient_id**: Patient ID
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    - **record_type**: Optional filter by record type
    """
    records = await PatientController.get_patient_medical_records(
        patient_id=patient_id,
        skip=skip,
        limit=limit,
        record_type=record_type,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        data=[{
            "id": str(record.id),
            "patient_id": str(record.patient_id),
            "record_type": record.record_type,
            "description": record.description,
            "record_date": record.record_date.isoformat() if record.record_date else None,
            "practitioner_id": str(record.practitioner_id) if record.practitioner_id else None,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        } for record in records],
        message=f"Retrieved {len(records)} medical records"
    )

@router.post("/{patient_id}/medical-records", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_medical_record(
    patient_id: str = Path(..., description="Patient ID"),
    record_data: Dict[str, Any] = Body(..., description="Medical record data"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
    db: Session = Depends(get_db)
):
    """
    Create a new medical record for a patient.
    
    - **patient_id**: Patient ID
    - **record_data**: Medical record data
    """
    record = await MedicalRecordController.create_medical_record(
        patient_id=patient_id,
        record_data=record_data,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        data={
            "id": str(record.id),
            "patient_id": str(record.patient_id),
            "record_type": record.record_type,
            "description": record.description,
            "record_date": record.record_date.isoformat() if record.record_date else None
        },
        message="Medical record created successfully"
    )
