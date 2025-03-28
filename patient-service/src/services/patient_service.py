from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
import uuid
from datetime import date

from ..models.patient import Patient
from ..models.medical_record import MedicalRecord
from ..models.attachment import Attachment
from ..models.patient_practitioner import PatientPractitioner

class PatientService:
    """
    Service for patient-related operations.
    """
    
    @staticmethod
    async def get_patients(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        user_id: Optional[str] = None,
        practitioner_id: Optional[str] = None
    ) -> List[Patient]:
        """
        Get a list of patients with optional filtering.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Optional search term for patient name
            user_id: Optional filter by user ID
            practitioner_id: Optional filter by practitioner ID
            
        Returns:
            List of patient records
        """
        query = db.query(Patient)
        
        # Apply filters if provided
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Patient.first_name.ilike(search_term)) | 
                (Patient.last_name.ilike(search_term)) |
                (Patient.email.ilike(search_term))
            )
            
        if user_id:
            query = query.filter(Patient.user_id == user_id)
            
        if practitioner_id:
            # Join with the patient_practitioners table to filter by practitioner
            query = query.join(
                PatientPractitioner, 
                Patient.id == PatientPractitioner.patient_id
            ).filter(
                PatientPractitioner.practitioner_id == practitioner_id
            )
            
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    async def get_patient_by_id(db: Session, patient_id: str) -> Optional[Patient]:
        """
        Get a patient by ID.
        
        Args:
            db: Database session
            patient_id: Patient ID
            
        Returns:
            Patient record or None if not found
        """
        return db.query(Patient).filter(Patient.id == patient_id).first()
    
    @staticmethod
    async def get_patient_by_user_id(db: Session, user_id: str) -> Optional[Patient]:
        """
        Get a patient by user ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Patient record or None if not found
        """
        return db.query(Patient).filter(Patient.user_id == user_id).first()
    
    @staticmethod
    async def create_patient(db: Session, patient_data: Dict[str, Any]) -> Patient:
        """
        Create a new patient.
        
        Args:
            db: Database session
            patient_data: Patient data
            
        Returns:
            Created patient record
            
        Raises:
            HTTPException: If there's an error creating the patient
        """
        try:
            patient = Patient(**patient_data)
            db.add(patient)
            db.commit()
            db.refresh(patient)
            return patient
        except IntegrityError as e:
            db.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A patient with this email already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating patient: {str(e)}"
            )
    
    @staticmethod
    async def update_patient(
        db: Session, 
        patient_id: str, 
        patient_data: Dict[str, Any]
    ) -> Optional[Patient]:
        """
        Update a patient.
        
        Args:
            db: Database session
            patient_id: Patient ID
            patient_data: Updated patient data
            
        Returns:
            Updated patient record or None if not found
            
        Raises:
            HTTPException: If there's an error updating the patient
        """
        patient = await PatientService.get_patient_by_id(db, patient_id)
        if not patient:
            return None
            
        try:
            for key, value in patient_data.items():
                setattr(patient, key, value)
                
            db.commit()
            db.refresh(patient)
            return patient
        except IntegrityError as e:
            db.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A patient with this email already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error updating patient: {str(e)}"
            )
    
    @staticmethod
    async def delete_patient(db: Session, patient_id: str) -> bool:
        """
        Delete a patient.
        
        Args:
            db: Database session
            patient_id: Patient ID
            
        Returns:
            True if deleted, False if not found
        """
        patient = await PatientService.get_patient_by_id(db, patient_id)
        if not patient:
            return False
            
        db.delete(patient)
        db.commit()
        return True
