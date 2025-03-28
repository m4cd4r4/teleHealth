from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid

from ..database import get_db
from ..services.patient_service import PatientService
from ..services.medical_record_service import MedicalRecordService
from ..utils.jwt_handler import get_current_user_with_roles

class PatientController:
    """
    Controller for patient-related operations.
    """
    
    @staticmethod
    async def get_patients(
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        user_id: Optional[str] = None,
        practitioner_id: Optional[str] = None,
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
        db: Session = Depends(get_db)
    ):
        """
        Get a list of patients with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Optional search term for patient name
            user_id: Optional filter by user ID
            practitioner_id: Optional filter by practitioner ID
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            List of patient records
        """
        # If the user is a practitioner, only return their patients
        if current_user.get("role") == "practitioner":
            practitioner_id = current_user.get("sub")
            
        return await PatientService.get_patients(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            user_id=user_id,
            practitioner_id=practitioner_id
        )
    
    @staticmethod
    async def get_patient_by_id(
        patient_id: str,
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner", "patient"])),
        db: Session = Depends(get_db)
    ):
        """
        Get a patient by ID.
        
        Args:
            patient_id: Patient ID
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            Patient record
            
        Raises:
            HTTPException: If patient not found or user doesn't have permission
        """
        patient = await PatientService.get_patient_by_id(db, patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        # Check permissions
        user_role = current_user.get("role")
        user_id = current_user.get("sub")
        
        # Patients can only access their own data
        if user_role == "patient" and str(patient.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this patient's data"
            )
            
        # Practitioners can only access their patients' data
        if user_role == "practitioner":
            # Check if the practitioner is assigned to this patient
            practitioner_patients = await PatientService.get_patients(
                db=db,
                practitioner_id=user_id
            )
            if patient not in practitioner_patients:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this patient's data"
                )
                
        return patient
    
    @staticmethod
    async def create_patient(
        patient_data: Dict[str, Any],
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner"])),
        db: Session = Depends(get_db)
    ):
        """
        Create a new patient.
        
        Args:
            patient_data: Patient data
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            Created patient record
        """
        # If user_id is not provided, use the current user's ID
        if "user_id" not in patient_data and current_user.get("role") == "patient":
            patient_data["user_id"] = current_user.get("sub")
            
        return await PatientService.create_patient(db, patient_data)
    
    @staticmethod
    async def update_patient(
        patient_id: str,
        patient_data: Dict[str, Any],
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner", "patient"])),
        db: Session = Depends(get_db)
    ):
        """
        Update a patient.
        
        Args:
            patient_id: Patient ID
            patient_data: Updated patient data
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            Updated patient record
            
        Raises:
            HTTPException: If patient not found or user doesn't have permission
        """
        # First check if the patient exists and user has permission
        await PatientController.get_patient_by_id(
            patient_id=patient_id,
            current_user=current_user,
            db=db
        )
        
        # Don't allow changing user_id
        if "user_id" in patient_data:
            del patient_data["user_id"]
            
        updated_patient = await PatientService.update_patient(db, patient_id, patient_data)
        if not updated_patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
            
        return updated_patient
    
    @staticmethod
    async def delete_patient(
        patient_id: str,
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin"])),
        db: Session = Depends(get_db)
    ):
        """
        Delete a patient.
        
        Args:
            patient_id: Patient ID
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If patient not found
        """
        # Only admins can delete patients
        deleted = await PatientService.delete_patient(db, patient_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
            
        return {"message": "Patient deleted successfully"}
    
    @staticmethod
    async def get_patient_medical_records(
        patient_id: str,
        skip: int = 0,
        limit: int = 100,
        record_type: Optional[str] = None,
        current_user: Dict[str, Any] = Depends(get_current_user_with_roles(["admin", "practitioner", "patient"])),
        db: Session = Depends(get_db)
    ):
        """
        Get a list of medical records for a patient.
        
        Args:
            patient_id: Patient ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            record_type: Optional filter by record type
            current_user: Current authenticated user
            db: Database session
            
        Returns:
            List of medical records
            
        Raises:
            HTTPException: If patient not found or user doesn't have permission
        """
        # First check if the patient exists and user has permission
        await PatientController.get_patient_by_id(
            patient_id=patient_id,
            current_user=current_user,
            db=db
        )
        
        return await MedicalRecordService.get_medical_records(
            db=db,
            patient_id=patient_id,
            skip=skip,
            limit=limit,
            record_type=record_type
        )
