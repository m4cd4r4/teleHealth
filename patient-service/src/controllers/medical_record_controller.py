from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid
from datetime import date

from ..database import get_db
from ..services.medical_record_service import MedicalRecordService
from ..utils.jwt_handler import get_current_user_with_roles
from .patient_controller import PatientController

class MedicalRecordController:
    """
    Controller for medical record-related operations.
    """
    
    @staticmethod
    async def create_medical_record(
        patient_id: str,
        record_data: Dict[str, Any],
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
        db: Session = Depends(get_db)
    ):
        """
        Create a new medical record for a patient.
        
        Args:
            patient_id: Patient ID
            record_data: Medical record data
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            Created medical record
            
        Raises:
            HTTPException: If patient not found or user doesn't have permission
        """
        # First check if the patient exists and user has permission
        await PatientController.get_patient_by_id(
            patient_id=patient_id,
            current_user=current_user,
            db=db
        )
        
        # Set the patient_id in the record data
        record_data["patient_id"] = patient_id
        
        # If practitioner_id is not provided, use the current user's ID if they are a practitioner
        if "practitioner_id" not in record_data and current_user.get("role") == "practitioner":
            record_data["practitioner_id"] = current_user.get("sub")
            
        return await MedicalRecordService.create_medical_record(db, record_data)
    
    @staticmethod
    async def get_medical_record_by_id(
        record_id: str,
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner", "patient"])),
        db: Session = Depends(get_db)
    ):
        """
        Get a medical record by ID.
        
        Args:
            record_id: Medical record ID
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            Medical record
            
        Raises:
            HTTPException: If record not found or user doesn't have permission
        """
        record = await MedicalRecordService.get_medical_record_by_id(db, record_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
            )
        
        # Check permissions by verifying access to the patient
        await PatientController.get_patient_by_id(
            patient_id=str(record.patient_id),
            current_user=current_user,
            db=db
        )
                
        return record
    
    @staticmethod
    async def update_medical_record(
        record_id: str,
        record_data: Dict[str, Any],
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
        db: Session = Depends(get_db)
    ):
        """
        Update a medical record.
        
        Args:
            record_id: Medical record ID
            record_data: Updated medical record data
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            Updated medical record
            
        Raises:
            HTTPException: If record not found or user doesn't have permission
        """
        # First check if the record exists and user has permission
        record = await MedicalRecordController.get_medical_record_by_id(
            record_id=record_id,
            current_user=current_user,
            db=db
        )
        
        # Don't allow changing patient_id
        if "patient_id" in record_data:
            del record_data["patient_id"]
            
        updated_record = await MedicalRecordService.update_medical_record(db, record_id, record_data)
        if not updated_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
            )
            
        return updated_record
    
    @staticmethod
    async def delete_medical_record(
        record_id: str,
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
        db: Session = Depends(get_db)
    ):
        """
        Delete a medical record.
        
        Args:
            record_id: Medical record ID
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If record not found or user doesn't have permission
        """
        # First check if the record exists and user has permission
        await MedicalRecordController.get_medical_record_by_id(
            record_id=record_id,
            current_user=current_user,
            db=db
        )
        
        # Only admins and practitioners can delete records
        deleted = await MedicalRecordService.delete_medical_record(db, record_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical record not found"
            )
            
        return {"message": "Medical record deleted successfully"}
