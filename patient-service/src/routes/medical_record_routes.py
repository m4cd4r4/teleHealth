from fastapi import APIRouter, Depends, Path, Body, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..database import get_db
from ..controllers.medical_record_controller import MedicalRecordController
from ..utils.response import success_response
from ..utils.jwt_handler import get_current_user_with_roles

# Create router
router = APIRouter(tags=["Medical Records"])

@router.get("/{record_id}", response_model=Dict[str, Any])
async def get_medical_record(
    record_id: str = Path(..., description="Medical record ID"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner", "patient"])),
    db: Session = Depends(get_db)
):
    """
    Get a medical record by ID.
    
    - **record_id**: Medical record ID
    """
    record = await MedicalRecordController.get_medical_record_by_id(
        record_id=record_id,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        data={
            "id": str(record.id),
            "patient_id": str(record.patient_id),
            "record_type": record.record_type,
            "description": record.description,
            "record_date": record.record_date.isoformat() if record.record_date else None,
            "practitioner_id": str(record.practitioner_id) if record.practitioner_id else None,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        },
        message="Medical record retrieved successfully"
    )

@router.put("/{record_id}", response_model=Dict[str, Any])
async def update_medical_record(
    record_id: str = Path(..., description="Medical record ID"),
    record_data: Dict[str, Any] = Body(..., description="Updated medical record data"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
    db: Session = Depends(get_db)
):
    """
    Update a medical record.
    
    - **record_id**: Medical record ID
    - **record_data**: Updated medical record data
    """
    record = await MedicalRecordController.update_medical_record(
        record_id=record_id,
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
            "record_date": record.record_date.isoformat() if record.record_date else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        },
        message="Medical record updated successfully"
    )

@router.delete("/{record_id}", response_model=Dict[str, Any])
async def delete_medical_record(
    record_id: str = Path(..., description="Medical record ID"),
    current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
    db: Session = Depends(get_db)
):
    """
    Delete a medical record.
    
    - **record_id**: Medical record ID
    """
    result = await MedicalRecordController.delete_medical_record(
        record_id=record_id,
        current_user=current_user,
        db=db
    )
    
    return success_response(
        message=result["message"]
    )
